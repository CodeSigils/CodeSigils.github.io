---
title: A Careful Samba Folder Share on Debian-Based Linux
description: A practical, safety-first SMB3-only Samba guide for sharing one or more local folders with Windows, macOS, and Linux devices on a home network, with the jargon explained.
keywords:
  - Samba
  - SMB3
  - Linux
  - Debian
  - file sharing
  - UFW
  - home network
icon: lucide/server
---

Sharing a folder on a home network should not require a cloud account, a USB disk passed from room to room, or a mystery configuration that nobody wants to touch again. Samba is a good fit when one Linux machine holds the files and the other devices use Windows, macOS, or Linux.

This guide builds one authenticated, SMB3-only share that's restricted to your local network, and [Step 11](#11-adding-another-share-later) shows how to add more folders later without disturbing the first. It walks through every step (mounting the disk, teaching Samba who may connect, writing the configuration, opening exactly one firewall port, and testing from each kind of client) and explains the technical terms as they appear.

Any tinkerer can make a share appear in a file browser by following some guide, without understanding the principles behind the moving parts or what is actually at stake. Beyond a working share, this guide is written as a learning opportunity: the project is one or more folders, and the concepts behind them are what you keep. The finished setup has clear boundaries (the disk is mounted, Samba knows who may connect, and the firewall admits only the local network), and you will understand why each piece is there when it comes time to maintain it.

Before the first command, it helps to know what Samba is beyond this evening's task. Think of it as the standard open-source bridge between Linux and the Windows world. It is what lets a Linux server join the account system many offices and schools run (Active Directory), and it can even act as the directory controller itself. The same software powers home NAS appliances and enterprise storage clusters alike, so this guide deliberately uses a small, well-worn corner of it: one standalone machine, one or more folders, no domain.

!!! warning "Replace all example values with your own"
This guide uses placeholders like `<your-user>`, `<your-interface>`, `<your-subnet>`, `<your-gateway>`, `<your-broadcast>`, `<server-ip>`, and `<UUID>`, alongside the example path `/mnt/one/KK_SHARE`. Don't copy these as-is. Run the inspection commands in [Step 1](#1-inspect-your-machine-first) and substitute the values you find for your system.

## A few terms worth knowing

If this is your first time sharing files on a Linux network, a handful of terms do most of the work. Everything later in the guide builds on them:

- **SMB** (Server Message Block) — the network protocol Windows uses to share files and printers. When you open `\\server\share` in File Explorer, you're speaking SMB.
- **Samba** — the free software that speaks SMB on Linux, so a Linux machine can offer folders that Windows, macOS, and other Linux systems understand.
- **smbd** — the Samba _daemon_, the background program that actually answers connection requests. "Daemon" just means a program that runs quietly in the background waiting for work; it's the thing `systemctl` starts and stops.
- **Share** — one folder made available on the network under a name (here, `KK_SHARE`). The _path_ (`/mnt/one/KK_SHARE`) is where the files live on Linux; the _share name_ is what clients see and type.
- **Mount** — attaching a disk's contents to a directory so Linux can reach them. Until a disk is mounted, its path looks like an ordinary — and misleadingly empty — directory.
- **Workgroup** — a loose label machines on a network use to find each other. The default `WORKGROUP` is fine for a home setup; it is a naming convention, not a security boundary.
- **UFW** (Uncomplicated Firewall) — a beginner-friendly front-end to the Linux firewall. It's what we'll use to admit only your local network.
- **Subnet and `/24`** — the range of addresses that make up your local network. You'll derive yours in Step 1; you never need to guess it.

## The three gates

It helps to think of a share as passing through three gates:

1. **The mount** — Linux must be looking at the intended disk, not an empty directory on its system drive. Get this wrong and you can end up creating files on the wrong filesystem without realising it.
2. **Samba** — a known account must authenticate before it may use the share. Without this, access is denied on purpose.
3. **The firewall** — only devices on the intended local network may reach Samba at all, on TCP port 445.

If a share fails, this model keeps the investigation calm. Check the gate closest to the file first, then work outward. It's the fastest way to avoid chasing ghosts.

---

## 1. Inspect Your Machine First

Before making changes, get a clear picture of your system. Start with a small map of the machine: these commands do not alter anything. They answer the questions that later steps depend on — which disk holds the files, which Linux account owns them, which address clients should use, and whether Samba or the firewall already has a configuration worth preserving.

Knowing this landscape saves a surprising amount of time. A command that is correct for one machine can point at the wrong disk, user, interface, or subnet on another. Capture the results before changing anything, then use your own values in the steps that follow.

```bash
# Check your distribution
cat /etc/os-release

# Confirm your Linux user exists and get its numeric IDs
getent passwd <your-user>
id <your-user>

# See disks, filesystems, labels, and UUIDs
lsblk -f

# See currently mounted NTFS filesystems (if any)
findmnt -t ntfs3,ntfs,fuseblk

# Inspect the filesystem for your share path
findmnt -T /mnt/one -o TARGET,SOURCE,FSTYPE,OPTIONS

# Check persistent mount configuration
grep -nE 'ntfs|fuseblk' /etc/fstab

# Check the directory structure for your share
ls -ld /mnt /mnt/one /mnt/one/KK_SHARE 2>/dev/null || ls -ld /mnt /mnt/one

# Check network interfaces and addresses
ip -o -f inet addr show
hostname -I
ip route

# Check Samba status (if installed)
systemctl is-active smbd; systemctl is-enabled smbd
dpkg -l samba samba-common samba-common-bin smbclient cifs-utils 2>/dev/null | grep -E '^(ii|un)'

# Check existing Samba config
command -v testparm >/dev/null && sudo testparm -s

# Check firewall
command -v ufw >/dev/null && sudo ufw status verbose
```

### Understanding what you just found

Every one of those commands prints something useful, and none of them changes the machine. Here is the real transcript from one machine that follows this guide — a PikaOS box with two NTFS disks — so you know what you are looking at. Your own output will differ in the details: disk UUIDs are shown as `<UUID>` here, network addresses as placeholders like `<server-ip>`, `<your-subnet>`, and the libvirt bridge addresses as `<libvirt-ip>`, `<libvirt-broadcast>`, and `<libvirt-net>`, the distribution file is trimmed to its identification fields, the `id` group list is cut short, and other disks are omitted from `lsblk`. Two names are deliberately left real: interface names such as `enp8s0` are structural labels that differ from machine to machine but reveal nothing sensitive, and `virbr0` is libvirt's default bridge name, the same string on every machine that has it:

```console
$ cat /etc/os-release
PRETTY_NAME="PikaOS 4"
NAME="PikaOS"
VERSION_ID="4"
VERSION_CODENAME=nest
ID=pika
ID_LIKE=debian
DEBIAN_CODENAME=sid

$ getent passwd <your-user>
<your-user>:x:1000:1000:<your-user>,,,/home/<your-user>:/bin/bash

$ id <your-user>
uid=1000(<your-user>) gid=1000(<your-user>) groups=1000(<your-user>),4(adm),27(sudo),100(users),…

$ lsblk -f
NAME        FSTYPE FSVER LABEL    UUID      FSAVAIL FSUSE% MOUNTPOINTS
└─sda2      ntfs         Store I  <UUID>        1.1T    40% /mnt/one
└─sdb2      ntfs         Store II <UUID>        1.2T    35% /mnt/two
# … other disks omitted

$ findmnt -t ntfs3,ntfs,fuseblk
TARGET   SOURCE    FSTYPE OPTIONS
/mnt/one /dev/sda2 ntfs3  rw,nosuid,nodev,relatime,uid=1000,gid=1000,dmask=0022,fmask=0133,discard,windows_names,acl,iocharset=utf8,prealloc
/mnt/two /dev/sdb2 ntfs3  rw,nosuid,nodev,relatime,uid=1000,gid=1000,dmask=0022,fmask=0133,discard,windows_names,acl,iocharset=utf8,prealloc

$ findmnt -T /mnt/one -o TARGET,SOURCE,FSTYPE,OPTIONS
TARGET   SOURCE    FSTYPE OPTIONS
/mnt/one /dev/sda2 ntfs3  rw,nosuid,nodev,relatime,uid=1000,gid=1000,dmask=0022,fmask=0133,discard,windows_names,acl,iocharset=utf8,prealloc

$ grep -nE 'ntfs|fuseblk' /etc/fstab
25:/dev/disk/by-uuid/<UUID> /mnt/two ntfs3 rw,relatime,nosuid,nodev,nofail,uid=1000,gid=1000,fmask=133,dmask=022,acl,windows_names,discard,x-gvfs-show,x-gvfs-name=two 0 0
26:/dev/disk/by-uuid/<UUID> /mnt/one ntfs3 rw,relatime,nosuid,nodev,nofail,uid=1000,gid=1000,fmask=133,dmask=022,acl,windows_names,discard,x-gvfs-show,x-gvfs-name=one 0 0

$ ls -ld /mnt /mnt/one /mnt/one/KK_SHARE
drwxr-xr-x 4 root root 4096 Feb  7  2026 /mnt
drwxrwxrwx 1 <your-user> <your-user> 4096 Oct  4 11:30 /mnt/one
drwxrwxr-x 1 <your-user> <your-user> 8192 Oct  4 16:55 /mnt/one/KK_SHARE

$ ip -o -f inet addr show
1: lo    inet 127.0.0.1/8 scope host lo\       valid_lft forever preferred_lft forever
2: enp8s0    inet <server-ip>/24 brd <your-broadcast> scope global dynamic noprefixroute enp8s0\       valid_lft 77620sec preferred_lft 77620sec
3: virbr0    inet <libvirt-ip>/24 brd <libvirt-broadcast> scope global virbr0\       valid_lft forever preferred_lft forever

$ hostname -I
<server-ip> <libvirt-ip>

$ ip route
default via <your-gateway> dev enp8s0 proto dhcp src <server-ip> metric 100
<your-subnet>/24 dev enp8s0 proto kernel scope link src <server-ip> metric 100
<libvirt-net>/24 dev virbr0 proto kernel scope link src <libvirt-ip> linkdown

$ systemctl is-active smbd; systemctl is-enabled smbd
active
enabled

$ dpkg -l samba samba-common samba-common-bin smbclient cifs-utils | grep -E '^(ii|un)'
ii  cifs-utils       2:7.4-1         amd64        Common Internet File System utilities
ii  samba            2:4.24.5+dfsg-1 amd64        SMB/CIFS file, print, and login server for Unix
ii  samba-common     2:4.24.5+dfsg-1 all          common files used by both the Samba server and client
ii  samba-common-bin 2:4.24.5+dfsg-1 amd64        Samba common files used by both the server and the client
ii  smbclient        2:4.24.5+dfsg-1 amd64        command-line SMB/CIFS clients for Unix

$ sudo testparm -s
Load smb config files from /etc/samba/smb.conf
Loaded services file OK.
Weak crypto is allowed by GnuTLS (e.g. NTLM as a compatibility fallback)

Server role: ROLE_STANDALONE

# Global parameters
[global]
	disable netbios = Yes
	disable spoolss = Yes
	load printers = No
	max log size = 1000
	security = USER
	server min protocol = SMB3_00
	server string = %h (PikaOS Samba)
	idmap config * : backend = tdb

[KK_SHARE]
	comment = KK_SHARE on PikaOS (/mnt/one)
	force user = <your-user>
	path = /mnt/one/KK_SHARE
	read only = No
	valid users = <your-user>
	vfs objects = fruit streams_xattr
	fruit:resource = file

$ sudo ufw status verbose
Status: active

To                         Action      From
--                         ------      ----
445/tcp                    ALLOW       <your-subnet>/24
```

The four questions worth answering from that transcript:

- **Network**: Look for your active interface (e.g. `enp0s3`, `eth0`, `wlan0`) and its IP address with CIDR (like `192.168.1.23/24`). `hostname -I` gives a quick list of the machine's current addresses; pair it with `ip route` to identify the active LAN address and default gateway. On a home network, an address such as `192.168.1.23/24` usually means the firewall subnet is `192.168.1.0/24` — confirm that from the actual route rather than copying the example.
- **Mount**: `findmnt -T /mnt/one` should show `TARGET` as exactly `/mnt/one`, with `SOURCE` and `FSTYPE` describing the disk you meant to share. If the target doesn't match, the disk isn't mounted there yet. An unmounted mount point still accepts `mkdir`, but any files created there land on the filesystem underneath it instead — which is exactly the kind of mistake that looks fine until you go looking for the files. The `FSTYPE` tells you if you're using `ntfs3` (in-kernel, recommended on modern kernels) or another filesystem.
- **Ownership**: For a single-user share, you'll want the share directory owned by `<your-user>`. Note the UID/GID from `id <your-user>` — you'll need this if setting up a persistent mount.
- **Existing configuration**: Read the service, package, Samba, and firewall output before making changes; an existing config may contain another share or a firewall rule you need to preserve. `dpkg -l` can return a non-zero status for an absent package — that's normal during this inspection. In its output, `ii` at the start of a line means the package is installed.

### A quick word on NTFS

NTFS and Linux do not model file ownership in the same way. NTFS is Microsoft's filesystem — it doesn't natively store the Unix-style user and group ownership that Linux expects. On an NTFS mount, options such as `uid=`, `gid=`, `fmask=`, and `dmask=` tell Linux how the files should _appear_ and which permissions new files receive. Linux writes permissions as compact base-eight numbers: `755` means the owner can read, write, and enter a directory, while everyone else can only read and enter it.

For a simple one-user NTFS share, Samba's `force user` setting (which we'll set in Step 6) ties everything together: after the network user has authenticated, Samba performs file work as one known Linux account. It does not replace authentication; it makes the filesystem side of the arrangement consistent.

---

## 2. Install Samba and Client Tools

Samba is packaged in every major Linux distribution, and installing it is ordinary package-manager work. On Debian, Ubuntu, PikaOS, and other APT-based systems, one command brings in the server and the two helpers this guide relies on:

```bash
sudo apt update
sudo apt install -y samba smbclient cifs-utils
```

- `samba` — the Samba server, including the `smbd` daemon
- `smbclient` — a command-line client, useful for testing connections locally before involving another device
- `cifs-utils` — provides the standard Linux mount helper for CIFS/SMB, used when another Linux machine mounts your share

Verify the service is installed and running:

```bash
systemctl is-active smbd
systemctl is-enabled smbd
```

The first command prints `active` when the service is running right now. The second prints `enabled` when the service is set to start after a reboot. You want to see exactly those two words.

---

## 3. Prepare a Persistent Mount (Recommended)

If your shared folder lives on a separate disk (especially NTFS), mount it persistently via `/etc/fstab` so it's still there after a reboot.
`/etc/fstab` is simply the file where Linux keeps its list of filesystems to mount at boot — each line is one disk, its mount point, its type, and a set of options.
Editing it feels intimidating because a mistake can affect startup, but the backup and test below catch problems long before a reboot.

### Which NTFS driver to use (and what to install)

Before the options, a package question that catches plenty of people out: NTFS is Windows' own filesystem, so Linux needs a driver for it, and there are two.

`ntfs3` lives inside the kernel itself.
It arrived in Linux 5.15 in late 2021, it needs no package at all, and it is generally the faster of the two.
Ubuntu 22.04 and newer, Fedora, and Arch all ship it in their stock kernels and load it automatically on the first mount attempt, so on those distributions there is nothing to install.
Debian 12 (kernel 6.1) is the notable exception: it does not include `ntfs3` at all, because Debian only enabled the driver with the Debian 13 kernel.
openSUSE builds it but blacklists it by default.
On such systems the `ntfs3` type simply does not exist, and the mount fails with:

```
mount: /mnt/one: unknown filesystem type 'ntfs3'.
```

The fix is one package: `ntfs-3g`.
That is the second driver, and it takes a different approach.
The NTFS code runs in userspace as an ordinary program, talking to the kernel through FUSE (Filesystem in Userspace, a mechanism that lets ordinary programs act as filesystem drivers).
It works on virtually any Linux, old or new, at the cost of some speed.
Install it, then use `ntfs-3g` as the filesystem type in the fstab line below instead of `ntfs3`.
Every option in the table below (`uid`, `gid`, `fmask`, `dmask`, and friends) works unchanged, because both drivers understand them.

- Debian or Ubuntu: `sudo apt install ntfs-3g` (the repair tools come bundled in the same package)
- Fedora: `sudo dnf install ntfs-3g ntfsprogs`
- Arch: `sudo pacman -S ntfs-3g ntfsprogs`
- openSUSE: `sudo zypper install ntfs-3g ntfsprogs`

Three footnotes, and then we move on.
Samba does not care which driver you choose: it shares the directory _after_ it is mounted, so the decision only affects this machine's own mount line.

Keep the `ntfs-3g` tools installed even when `ntfs3` does the mounting, because `ntfs3` ships no checking or repair tools of its own; `ntfsfix` and the rest come from the ntfs-3g side of the house.

And if `ntfs3` already mounts your disk today, leave it alone. Nothing in this guide requires a switch.

Two small exceptions worth knowing before you paste the options below.

- One, the fstab line spells the filesystem type out on purpose: with recent versions of util-linux,
  a bare `mount -t auto` may pick a different NTFS driver than the one you expect.

- Two, the `windows_names` option was added to `ntfs3` only in more recent kernels (roughly 6.6 and newer),
  so if an `ntfs3` mount refuses to start and the kernel log complains about an unrecognized option,
  drop that one option from the line; `ntfs-3g` has always accepted it.

### Understand your mount options (especially for NTFS)

If you're working with NTFS, the mount options matter more than they might seem at first — they're the mechanism described in [A quick word on NTFS](#a-quick-word-on-ntfs) above, in practice.
Here is every option this guide uses:

| Option                    | Purpose                                                                                                                                                                                                                  |
| :------------------------ | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `rw`                      | Mount read-write. Required for a writable share.                                                                                                                                                                         |
| `relatime`                | Updates access time only when needed (better for SSDs and reduces I/O).                                                                                                                                                  |
| `nosuid`/`nodev`          | Safety: ignores setuid/setgid bits and device files on this volume.                                                                                                                                                      |
| `nofail`                  | If the disk isn't present at boot, continue booting rather than dropping to emergency mode. Good for removable/data drives.                                                                                              |
| `uid=<uid>` / `gid=<gid>` | For NTFS (which has no Unix ownership), these make all files appear owned by that Linux user/group. Get these from `id <your-user>`.                                                                                     |
| `fmask=133` / `dmask=022` | For NTFS, control permissions. `fmask=133` gives files `644` (owner rw, others r), `dmask=022` gives dirs `755` (owner rwx, others rx). This keeps permissions sensible while allowing the designated user full control. |
| `acl`                     | Enables POSIX ACLs on the NTFS volume (useful for more granular control if needed).                                                                                                                                      |
| `windows_names`           | Prevents creating filenames that Windows cannot open (reserved names, trailing spaces, invalid characters).                                                                                                              |
| `discard`                 | Enables TRIM for SSDs (harmless on HDDs).                                                                                                                                                                                |

!!! warning "A small trap to avoid"
On NTFS, the `fmask`/`dmask` you set here effectively cap what Samba can do. Even if you set Samba's `create mask`/`directory mask` higher, they can't grant permissions the mount takes away. This is exactly why we pair the mount with `force user` later in the Samba config.

### Add your mount to /etc/fstab

First, back up your fstab — a timestamped copy you can always fall back on:

```bash
sudo cp /etc/fstab /etc/fstab.bak.$(date +%Y%m%d_%H%M%S)
```

Then edit `/etc/fstab` (`sudoedit /etc/fstab`) and add a line for your disk. Use the UUID from `lsblk -f` — it's a disk's unique identifier, stable even if device names like `/dev/sdb1` change between boots.

```text
# Share volume (NTFS with user ownership)
UUID=<UUID>  /mnt/one  ntfs3  rw,relatime,nosuid,nodev,nofail,uid=<uid>,gid=<gid>,fmask=133,dmask=022,acl,windows_names,discard  0  0
```

The two trailing zeros are real settings, not decoration. The first is the dump field: `0` tells the backup tool `dump` to skip this filesystem. The second is the fsck field: `0` tells the boot-time filesystem check to skip it too. Both are the right choice for a data volume like an NTFS drive. On systemd systems it is also good practice to run `sudo systemctl daemon-reload` after editing fstab, so the running system picks up the new line without waiting for a reboot.

Test the mount without rebooting:

```bash
sudo mount -a
findmnt -T /mnt/one
```

`mount -a` reads `/etc/fstab` and mounts everything listed in it (apart from lines marked `noauto`), so it's a safe way to prove your new line works without rebooting. It doesn't stop at the first failure, so read any error output it prints; silence means every line worked. If `findmnt` then shows the correct options, your persistent mount is working.

---

## 4. Create the Share Directory

With the disk mounted, the share itself is nothing more than a folder. Create it and hand it to the Linux account that will own it:

```bash
sudo mkdir -p /mnt/one/KK_SHARE
sudo chown <your-user>:<your-user> /mnt/one/KK_SHARE
sudo chmod u+rwx,go-rwx /mnt/one/KK_SHARE
ls -ld /mnt/one/KK_SHARE
```

The `-p` means the command succeeds quietly if the directory already exists, and it never removes anything. The `chown` and `chmod` below are deliberately non-recursive too — they set up the folder itself, not any content you may already have inside it. (Step 11 uses plain `mkdir` on purpose: without `-p`, an existing directory makes the command fail and gives you a chance to stop and inspect it first.)

You should see the directory owned by `<your-user>` with permissions `drwx------` (owner can read, write, and enter; nobody else can). On NTFS, the effective permissions are shaped by the mount options above instead. Check the final `ls -ld` output rather than assuming every NTFS mount handles later `chown` and `chmod` calls in the same way — and don't try to "fix" it by loosening mount options until you understand what they're doing.

---

## 5. Create the Samba User

Samba keeps its own password record, separate from your Linux login password unless a system is deliberately configured to synchronise them. Type your Linux username and a password for it, and Samba stores it in its own database. Create and enable a Samba account:

```bash
sudo smbpasswd -a <your-user>
sudo smbpasswd -e <your-user>
sudo pdbedit -L
```

- `smbpasswd -a` adds the account and asks for a Samba password.
- `smbpasswd -e` enables it — a disabled account masquerades as a wrong password, which sends you hunting in the wrong direction.
- `pdbedit -L` lists the accounts Samba knows about.

The password doesn't need to match your Linux login password — it's the password clients will use to connect to the share. `pdbedit -L` confirming your account exists is good evidence, but a real connection test in Step 9 is still the final proof that the password works.

---

## 6. Configure Samba

Everything so far has prepared the ground: the disk is mounted, the folder exists, and Samba has a password for you. What remains is giving Samba its instructions, and they live in one file: `/etc/samba/smb.conf`.

A good home configuration follows a few quiet conventions. Back up the old file before you touch it, so every change stays reversible. Give each line a reason you could explain to someone else, and leave everything else at Samba's default: a short configuration you understand beats a long one you don't, and the defaults have already been tested by thousands of installations. With those conventions in place, the actual work is small.

### Back up your existing config

A timestamped copy, so several backups can coexist and you can always diff the current file against the newest one:

```bash
sudo cp /etc/samba/smb.conf /etc/samba/smb.conf.bak.$(date +%Y%m%d_%H%M%S)
```

### Write the secure configuration

Edit `/etc/samba/smb.conf` (`sudoedit /etc/samba/smb.conf`). If you already have other shares configured, preserve them — only replace/add what you need. For a fresh setup, use this minimal, SMB3-only configuration:

```ini
[global]
    # Identification
    workgroup = WORKGROUP
    server string = %h Samba Server

    # Protocol: SMB3 only, no NetBIOS
    server min protocol = SMB3_00
    server max protocol = SMB3_11
    disable netbios = yes

    # Authentication
    security = user
    ntlm auth = ntlmv2-only

    # Disable printer support (not needed for file sharing)
    load printers = no
    disable spoolss = yes

    # Logging
    max log size = 1000

[KK_SHARE]
    comment = Private LAN share
    path = /mnt/one/KK_SHARE
    browseable = yes
    read only = no
    guest ok = no
    valid users = <your-user>

    # Pin all operations to the designated user (critical for NTFS mounts)
    force user = <your-user>

    # Apple metadata support for macOS/iOS clients (Finder and Files previews)
    vfs objects = fruit streams_xattr
    fruit:resource = file
```

### Why these choices matter

The important lines are deliberately plain:

- **SMB3-only** (`server min protocol = SMB3_00`, `server max protocol = SMB3_11`): Blocks legacy SMB1/SMB2 connections — SMB1 is decades old and has known security problems. Modern clients (Windows 10+, macOS, current Linux) support SMB3 just fine.
- **No NetBIOS** (`disable netbios = yes`): SMB3 works over TCP port 445 directly. Disabling NetBIOS removes legacy name resolution and the associated ports (137–139), so the firewall only ever needs one rule.
- **Authenticated access only** (`security = user`, `guest ok = no`, `valid users = <your-user>`): Every connection must authenticate as your specified user. There is no anonymous "everyone" path.
- **`force user = <your-user>`**: Ensures all file work happens as that Linux user — the setting promised back in [A quick word on NTFS](#a-quick-word-on-ntfs). It matters most on NTFS mounts where ownership is synthesised. Skip it and you can end up with files owned in a way that looks fine from Samba but causes confusion when you look at them directly on the Linux filesystem. It's a small setting that prevents a lot of head-scratching later.
- **`ntlm auth = ntlmv2-only`**: Allows the modern NTLMv2 authentication method and refuses the weaker old variants.
- **`vfs objects = fruit streams_xattr`**: Loads Samba's Apple compatibility modules for this share. `fruit` enables Apple's SMB2+ extension (AAPL) and handles the macOS-specific metadata that Finder and the iOS Files app expect during directory reads; `streams_xattr` supplies the named-stream storage that `fruit` defers to for everything it does not handle itself. Order matters — `fruit` must come before `streams_xattr`. These are per-share settings: they belong inside the `[KK_SHARE]` block, not `[global]`, and a share section that sets `vfs objects` replaces (does not merge with) a global one.
- **`fruit:resource = file`**: Stores larger resource forks as `._` AppleDouble sidecar files instead of filesystem extended attributes. This is the default and the safe choice on Linux — the `xattr` alternative only works on filesystems with large-xattr support such as ZFS or Solaris, and `stream` is marked experimental.
- **Why bother?** Without these lines, macOS and iOS clients still connect and transfer files, but Apple-specific metadata has nowhere to live. The visible symptom is in Finder and the iOS Files app: previews show **"File preview not available"** (or the file simply won't open in Quick Look) until you disconnect and reconnect. The share works otherwise, which is exactly why it is easy to miss. One practical note: `streams_xattr` needs user extended attributes to actually work on the underlying filesystem — on Linux this is standard for ext4/btrfs/xfs, but if previews still fail (common with some NTFS mounts), verify with a quick probe before blaming the config:

  ```bash
  probe=$(mktemp /tmp/.samba-xattr-probe.XXXXXX)
  gio set -t string "$probe" xattr::user.samba_fruit_probe verified
  gio info -a 'xattr::user.samba_fruit_probe' "$probe"
  gio remove "$probe" xattr::user.samba_fruit_probe; rm -f "$probe"
  ```

  If the attribute round-trips, the storage side is fine; reconnect the macOS/iOS client after `sudo systemctl restart smbd` and the previews return. `fruit:aapl` defaults to `yes` in current Samba, so it needs no explicit line.

This is a single-user home-network example. A family share, an office, an Active Directory domain, or access from outside the home deserves a different identity and security design.

### Validate the configuration

Before restarting, test that Samba can parse your config:

```bash
sudo testparm -s
```

Never make a syntax test depend on whether a service happened to restart. `testparm -s` shows the configuration exactly as Samba parsed it, so a mistake surfaces here — while the old, working config is still the one running. You should see `[global]` and `[KK_SHARE]` in the dump, and the line `Loaded services file OK.` confirms the file parsed. A completely broken file prints `Error loading services.` instead and exits with a non-zero status; that is the moment to fix, not to restart.

Do not be alarmed when lines you wrote seem to vanish. `testparm` omits every setting that equals Samba's built-in default, so `workgroup`, `ntlm auth`, `guest ok`, `browseable`, and `server max protocol` are all absent from a healthy dump — that is normal, not a failed save. Conversely, one line you never wrote may appear anyway: `idmap config * : backend = tdb`, which Samba injects into every load. The dump also normalizes what it prints: `security = user` comes back as `security = USER`, and yes/no settings as `Yes` or `No`.

Finally, look for `Server role: ROLE_STANDALONE` — it confirms a standalone, non-domain-joined server, which is what this guide builds. A `WARNING:` line about a deprecated option is usually a reminder rather than a failure, but any `ERROR:` line or non-zero exit status deserves a careful read before you continue. You may also see informational messages such as the GnuTLS weak-crypto note; these are normal and not related to your config.

---

## 7. Apply and Start Samba

Until now, the configuration has been text on a disk; the running service only reads it when it restarts, which is why validation came first. Two commands finish the job: one loads the new configuration now, the other makes Samba return after a reboot. Run them only once `testparm` passes:

```bash
sudo systemctl restart smbd
sudo systemctl enable smbd
systemctl is-active smbd
```

If `smbd` fails to start, run `sudo testparm -s` and `journalctl -u smbd -n 50 --no-pager` to see the error details. If it fails right after editing, your last change is usually the culprit.

One more habit worth keeping: after any Samba upgrade, run `sudo testparm -s` again. Options that were fine yesterday can start emitting deprecation warnings once a new version arrives, and the Samba project explicitly asks users to re-run `testparm` after upgrading — it is the cheapest health check there is.

---

## 8. Restrict Access to Your Local Network (Firewall)

A firewall decides which network traffic is allowed through. Only SMB should come from your home network — nothing else on the internet needs to reach TCP 445. First identify the real local subnet:

```bash
ip -4 addr show <your-interface>
ip route | grep default
```

For most home routers, if your IP is `192.168.1.XX/24`, your subnet is `192.168.1.0/24`. The `/24` is compact notation for all addresses beginning with `192.168.1.`. Adjust if yours differs (common alternatives: `10.0.0.0/24`, `172.16.0.0/24`). Your network may be different — the safety property is the narrow source range, not the example numbers.

Allow TCP port 445 from that subnet only:

```bash
sudo ufw allow from <your-subnet>/24 to any port 445 proto tcp
sudo ufw status verbose
```

You should see exactly one rule allowing `445/tcp` from `<your-subnet>/24`. If the list also shows an older, wider rule for the same port (one that says `Anywhere`), remove it by its number:

```bash
sudo ufw status numbered
sudo ufw delete <number>
```

UFW asks `Proceed with operation (y|n)?` before deleting, so you get a chance to check you have picked the right row. A wider rule left behind would quietly undo the restriction this section just built.

!!! warning "Enabling a firewall is a separate decision"
If UFW isn't enabled yet, do not enable it blindly — especially on a remote machine. Make sure the firewall already permits the management access you need (SSH or your management port: `sudo ufw allow ssh`) before running `sudo ufw enable`. It's easy to get distracted and enable UFW before adding that rule; if that happens, you can lock yourself out of remote access.

!!! note "Supporting very old devices"
With NetBIOS disabled and SMB3 required, the old 137–139 NetBIOS ports are not part of this setup. If you absolutely must support a very old device that can't do SMB3, you'd need to open those ports and lower `server min protocol`. This guide doesn't cover that — SMB3-only is the recommended, safer default. If you go down that route, keep that device isolated as much as you can. For most home networks, it's simply not needed anymore.

---

## 9. Test the Share

A configuration that parses is not yet a share; it is only a promise. Testing is where the three gates meet, and the order matters as much as the tests themselves. Start on the server itself, where only the mount and Samba can be at fault, and move to another device once that passes, so a failure at any point points at exactly one gate. When everything works, confirm the negotiated protocol instead of assuming it: a login that succeeds proves authentication, not SMB3.

### Test locally on the server first

The server can test the same SMB path a client uses:

```bash
# List shares (forcing SMB3)
smbclient -L //127.0.0.1 -U <your-user> --option='client min protocol=SMB3_00'

# Connect to the share interactively
smbclient //127.0.0.1/KK_SHARE -U <your-user> --option='client min protocol=SMB3_00'
```

`127.0.0.1` is the machine itself (localhost), so this test skips the firewall and your home network entirely. From inside the `smbclient` prompt, test write access:

```text
ls
mkdir testdir
rmdir testdir
quit
```

If these succeed without errors, authentication and filesystem permissions are working correctly. Only the network gates remain.

### Test from another device on your LAN

Now test from another device on the same network using `<server-ip>` (the IP you found in step 1, e.g. `192.168.1.23`). Use the server's current IP address if local DNS or name discovery is not part of your network — that's less elegant than a hostname, but far easier to diagnose.

**Windows (File Explorer):** Open `\\<server-ip>\KK_SHARE`. When prompted, enter `<your-user>` and your Samba password. If Windows insists the password is wrong, it is usually holding an old one. Windows keeps credentials in two separate places, so clear both: delete the saved entry for `<server-ip>` in Credential Manager, and run `net use * /delete` to drop any open sessions.

**macOS (Finder):** Go → Connect to Server → `smb://<server-ip>/KK_SHARE`. macOS uses SMB 3 by default. Authenticate with `<your-user>` and your Samba password; if a dialog asks for a workgroup name, `WORKGROUP` is the correct answer. If the connection fails without ever prompting for a password, try `smb://<your-user>:*@<server-ip>/KK_SHARE` (the `*` is a placeholder that tells macOS to ask for the password).

**Linux (temporary mount):**

```bash
mkdir -p ~/smbtest
sudo mount -t cifs //<server-ip>/KK_SHARE ~/smbtest -o uid=$(id -u),gid=$(id -g),vers=3.1.1,username=<your-user>,sec=ntlmssp
# Enter Samba password when prompted
findmnt -T ~/smbtest
touch ~/smbtest/.probe && rm ~/smbtest/.probe  # Test write
sudo umount ~/smbtest
```

If the mount fails with `error(95) Operation not supported`, try `vers=3.0` instead of `3.1.1`. `seal` (encryption) is optional — you can add it if desired, but not all clients need it. Error 95 is Samba's generic "this dialect or feature is not supported" complaint, so an explicit `vers=` plus dropping `seal` if you added it resolves the usual cases.

### Confirm the protocol actually negotiated

A successful login proves authentication; it does not by itself prove SMB3 was used. On the server, run:

```bash
smbstatus -b
```

The `Protocol Version` column shows what each session actually negotiated — `SMB3_11`, `SMB3_10`, `SMB3_02`, or `SMB3_00` for the SMB3 family. Anything in the `SMB2_...` range means a client slipped below your configured minimum, which is worth understanding before you trust the setup.

For a stricter check, ask a client to negotiate an older dialect and confirm the server refuses it:

```bash
smbclient -L //<server-ip> -U <your-user> --option='client max protocol=SMB2'
```

This should fail with a protocol negotiation error — exactly what a server with `server min protocol = SMB3_00` is supposed to do when a client asks for anything older.

---

## 10. Troubleshooting

Everything worked yesterday. Today the laptop reports a wrong password, or the share has quietly vanished from the file browser, and the natural reaction is to start changing settings until something improves. That reaction is understandable, and it is also how a one-line fix turns into an evening of mystery. Most Samba problems live in one of a few places; finding them is a matter of order rather than luck.

### Troubleshooting in a useful order

When a client cannot connect, work from the local system outward:

1. `findmnt -T /mnt/one -o TARGET,SOURCE,FSTYPE,OPTIONS` — is the intended disk mounted?
2. `sudo testparm -s` — does Samba accept the configuration?
3. `systemctl is-active smbd` — is the service running?
4. `smbclient -L //127.0.0.1 -U <your-user>` — does the server work locally?
5. `sudo ufw status numbered` — is TCP 445 allowed from, and limited to, the intended LAN?
6. Test another device using the server IP address.

This order separates disk, configuration, service, authentication, and network problems — the three gates, checked from the inside out. It is much quicker than changing several things at once and hoping one of them helped.

### By symptom

One term first: `veto files` is an optional setting that hides files matching a pattern list (old tutorials often add it). This guide's configuration doesn't include it — but if your `smb.conf` does, the last three rows apply.

| Symptom                                              | Likely Cause                               | Fix                                                                                                                                                                                                                |
| ---------------------------------------------------- | ------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Windows says "incorrect password" but it is correct  | Cached credentials                         | Clear the saved entry in Credential Manager, then run `net use * /delete` to drop open sessions; the two are separate stores. If it still refuses, try `.\<your-user>` as the username.                            |
| Share not found from other devices                   | Firewall, service not running, or wrong IP | Check `systemctl is-active smbd`, `sudo ufw status`, and confirm you're using the correct `<server-ip>` from the same subnet.                                                                                      |
| Can connect but get "permission denied" when writing | Filesystem permissions/mount options       | Verify `findmnt -T /mnt/one` shows expected options. Check ownership with `ls -ld /mnt/one/KK_SHARE`. Ensure `force user = <your-user>` is in smb.conf and the user matches.                                       |
| `smbd` won't start                                   | Config syntax error                        | Run `sudo testparm -s` to catch parse errors. Check `journalctl -u smbd -n 50 --no-pager` for details. If it fails right after editing, your last change is usually the culprit.                                   |
| Dotfiles invisible                                   | Veto patterns                              | If `veto files` includes `.*`, that hides dotfiles. Remove or narrow that pattern if you need to see them.                                                                                                         |
| Directory deletion fails saying "not empty"          | Hidden files (like `.DS_Store` from macOS) | Add `delete veto files = yes` under the share if you want Samba to clean up vetoed files on deletion. This is convenient, but be deliberate about it - it means Samba will remove files that match your veto list. |
| Slow directory listings with many files              | Broad veto patterns                        | Narrow your `veto files` pattern - scanning against many patterns is expensive.                                                                                                                                    |
| macOS/iOS preview says "File preview not available"  | Missing Apple metadata modules             | Add `vfs objects = fruit streams_xattr` and `fruit:resource = file` to the share section (see [Why these choices matter](#why-these-choices-matter)), run `sudo testparm -s`, restart `smbd`, then disconnect and reconnect the client. |

!!! note "AppArmor on Ubuntu and similar systems"
Ubuntu ships AppArmor profiles for Samba. A profile in _complain_ mode only logs what it would block; in enforce mode it actually denies access. Run `sudo aa-status` to see whether profiles for `smbd` are loaded, look for `AppArmor: ... DENIED` entries in `/var/log/syslog` when a path fails for no visible reason, and check `/sys/kernel/security/lsm` to see which security modules are active at all.

### Quick diagnostic commands

Four questions cover most situations where the answer isn't obvious: what sessions does the server actually see, what files are open right now, what is Samba saying at this moment, and what changed in the configuration since the last copy you knew was good? None of these commands change anything — they are a report, not a repair, which is why they are safe to run at any point in the troubleshooting order.

```bash
# Check active connections and negotiated protocol
smbstatus -b

# View open shares and file handles
smbstatus -S

# Tail Samba logs in real-time
tail -f /var/log/samba/log.smbd

# Compare current config with your most recent backup
ls -lt /etc/samba/smb.conf.bak.* | head -1
sudo diff -u $(ls -t /etc/samba/smb.conf.bak.* | head -1) /etc/samba/smb.conf
```

- **`smbstatus -b`** lists each active session together with the protocol version it negotiated. It answers the question clients rarely report accurately: whether a connection exists at all, and whether it arrived at SMB3 or fell back. A login attempt that failed on the server never appears here, so an empty list during a failed test is itself a clue — the problem is authentication or earlier, not the share itself.
- **`smbstatus -S`** shows which shares are open and which file handles are in use. When Windows refuses to rename a directory, or a file is locked by "another user", the holder is usually a session you cannot see from the file manager, and this is where it shows up.
- **`tail -f /var/log/samba/log.smbd`** streams the server's own account of events while you work. The client reports a symptom ("network path not found"); the log gives the reason behind it. Leave it running, retry the failing action on the client, and read the lines that appear — then Ctrl+C.
- **The `diff`** compares the live `smb.conf` against your newest backup, the last state you deliberately wrote. If trouble started right after an edit, this isolates the change instead of inviting you to re-read the whole file; the leading `ls -lt` simply shows you which backup is newest before the comparison picks it automatically. The `-u` flag adds surrounding context, so a line that merely moved looks different from one that was added or removed.

---

## 11. Adding Another Share Later

To add another folder, **append** to `smb.conf` — never overwrite the whole file. This preserves your existing shares.

```bash
# Verify the new mount/path exists and is mounted
findmnt -T /mnt/two

# Create the directory
sudo mkdir /mnt/two/ANOTHER_SHARE
sudo chown <your-user>:<your-user> /mnt/two/ANOTHER_SHARE
sudo chmod u+rwx,go-rwx /mnt/two/ANOTHER_SHARE

# Back up
sudo cp /etc/samba/smb.conf /etc/samba/smb.conf.bak.$(date +%Y%m%d_%H%M%S)

# Append the new share stanza
sudo tee -a /etc/samba/smb.conf > /dev/null << 'CONF'

[ANOTHER_SHARE]
    comment = Second private LAN share
    path = /mnt/two/ANOTHER_SHARE
    browseable = yes
    read only = no
    guest ok = no
    valid users = <your-user>
    force user = <your-user>
    vfs objects = fruit streams_xattr
    fruit:resource = file
CONF

# Validate and restart
sudo testparm -s
sudo systemctl restart smbd
```

A few notes on what just happened:

- The `-a` in `tee -a` means _append_ — add to the end without replacing what's there.
- The text between `<< 'CONF'` and the final `CONF` is a here-document: a tidy way to pass several lines of text to one command. The quoted marker prevents the shell from expanding anything inside it, so your `<your-user>` placeholder stays literal.
- Check the new path with `findmnt` first. An absent disk can leave behind an empty-looking mount point, and that is exactly the kind of problem a little preparation prevents.
- The name inside `[...]` becomes the folder name clients see, so choose it deliberately. Avoid `/` and `\` — the SMB specification forbids them in share names even though Samba's parser accepts them, and Windows addressing (`\\server\share`) depends on those characters staying special. Spaces are legal but behave inconsistently across clients, so a name like `ANOTHER_SHARE` is the safe habit. Do not reuse the special section names `[global]`, `[homes]`, or `[printers]`, and leave `print$` and `IPC$` alone — Windows treats those as its own. A name that _ends_ in `$` still works but is hidden from browse lists, which is how administrative shares stay out of sight.
- No new firewall rules are needed — Samba is already listening on TCP 445 for your LAN.

---

## Keep the reasoning with the commands

Once everything works, it is tempting to close the terminal and forget the whole exercise. Before that happens, it is worth leaving behind a small record of what was checked, why the firewall is narrow, and how to add the next share without undoing the first one. It turns a one-evening repair into a configuration you can reuse during a rebuild or adapt for another machine.

---

## Further Reading

Samba's own documentation:

- [What Is Samba?](https://www.samba.org/samba/what_is_samba.html) - The project's own plain-language answer, and where the intro's summary comes from
- [Samba Official Documentation](https://www.samba.org/samba/docs/) - Complete reference for Samba
- [smb.conf(5) Manual](https://www.samba.org/samba/docs/current/man-html/smb.conf.5.html) - All configuration options explained
- [smbd(8) Manual](https://www.samba.org/samba/docs/current/man-html/smbd.8.html) - The server daemon your `systemctl` commands start and stop
- [testparm(1) Manual](https://www.samba.org/samba/docs/current/man-html/testparm.1.html) - The validation tool from Step 6, with its exit codes explained
- [smbpasswd(5) Manual](https://www.samba.org/samba/docs/current/man-html/smbpasswd.5.html) - How Samba stores its password database, separate from Linux logins
- [smbstatus(1) Manual](https://www.samba.org/samba/docs/current/man-html/smbstatus.1.html) - The connection and protocol inspection used in Step 9
- [Standalone server role (smb.conf(5))](https://www.samba.org/samba/docs/current/man-html/smb.conf.5.html#server-role-g) - Why `testparm` reports `ROLE_STANDALONE`
- [Samba Server Security](https://www.samba.org/samba/docs/server_security.html) - Deeper dive into hardening
- [vfs_fruit(8) Manual](https://www.samba.org/samba/docs/current/man-html/vfs_fruit.8.html) - The Apple metadata module used in Step 6, with every `fruit:` option explained
- [Configure Samba to Work Better with Mac OS X (SambaWiki)](https://wiki.samba.org/index.php/Configure_Samba_to_Work_Better_with_Mac_OS_X) - Community-maintained fruit tuning guide, including Time Machine shares

The system side:

- [Linux NTFS3 Driver Docs](https://docs.kernel.org/filesystems/ntfs3.html) - Details on NTFS mount options
- [fstab(5) Manual](https://man7.org/linux/man-pages/man5/fstab.5.html) - The six fields of an fstab line, including the trailing `0  0`
- [UFW Firewall Guide (Ubuntu)](https://documentation.ubuntu.com/server/how-to/security/firewalls/) - UFW concepts and best practices

When clients misbehave:

- [Samba AppArmor Profile (Ubuntu)](https://ubuntu.com/server/docs/how-to/samba/apparmor-profile/) - What to check when access is denied for no visible reason
- [ArchWiki: Samba](https://wiki.archlinux.org/title/Samba) - A densely practical community guide, excellent for odd client-specific problems

---

_Reviewed 2026-10-05. Packages, defaults, and kernel behavior change over time - it's worth a quick sanity check against your specific system before running unfamiliar commands._
