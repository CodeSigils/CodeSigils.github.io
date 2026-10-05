---
title: A Careful Samba Folder Share on Debian-Based Linux
description: A practical SMB3-only Samba guide for sharing one local folder safely with Windows, macOS, and Linux devices on a home LAN.
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

Sharing a folder on a home network should not require a cloud account, a USB
disk passed from room to room, or a mystery configuration that nobody wants to
touch again. Samba is a good fit when one Linux machine holds the files and the
other devices use Windows, macOS, or Linux.

This guide builds one authenticated, SMB3-only share for a local network. It
uses `/mnt/one/KK_SHARE` and the example account `youruser`. Treat those as
names to replace, not values to copy blindly.

The point is not merely to make a share appear in a file browser. It is to
leave behind a setup that has clear boundaries: the disk is mounted, Samba
knows who may connect, and the firewall admits only the local network.

!!! warning "Examples are not your machine"

    Replace `youruser`, `/mnt/one`, `KK_SHARE`, `192.168.1.0/24`, and
    `enp0s3` with values from your own system. Never copy another machine's
    disk UUID, IP address, username, or firewall subnet.

## The three gates

It helps to think of a share as passing through three gates:

1. **The mount:** Linux must be looking at the intended disk, not an empty
   directory on its system drive.
2. **Samba:** a known account must authenticate before it may use the share.
3. **The firewall:** only devices on the intended LAN may reach Samba at all.

If a share fails, this model keeps the investigation calm. Check the gate
closest to the file first, then work outward.

## 1. Inspect the machine before changing it

Start with facts. These commands do not alter the system.

```bash
# Distribution and package manager
cat /etc/os-release

# The filesystem that actually contains the future share
findmnt -T /mnt/one -o TARGET,SOURCE,FSTYPE,OPTIONS

# Persistent mount declarations, if any
grep -nE 'ntfs|fuseblk' /etc/fstab

# Network interfaces and routes
ip -o -f inet addr show
ip route

# Existing Samba configuration and firewall state
sudo testparm -s
sudo ufw status verbose
```

The first `findmnt` result is especially important. Its `TARGET` column should
be exactly `/mnt/one`, and its `SOURCE` and `FSTYPE` should describe the disk
you meant to share. An unmounted mount point still accepts `mkdir`, but any
files created there land on the filesystem underneath it instead.

### A quick word on NTFS

NTFS and Linux do not model file ownership in the same way. On a Linux mount,
options such as `uid=`, `gid=`, `fmask=`, and `dmask=` control how the files
appear to Linux and which permissions new files receive. Linux writes modes as
compact base-eight numbers: `755` means the owner can read, write, and enter a
directory, while everyone else can read and enter it.

For a simple one-user NTFS share, Samba's `force user` setting is useful: after
the network user has authenticated, Samba performs file work as one known Linux
account. It does not replace authentication; it makes the filesystem side of
the arrangement consistent.

## 2. Install Samba and the client tools

On Debian, PikaOS, Ubuntu, and similar APT-based systems:

```bash
sudo apt update
sudo apt install -y samba smbclient cifs-utils
```

`samba` runs the server. `smbclient` lets the server test itself locally, and
`cifs-utils` supplies the normal Linux mount helper for another Linux client.

Confirm that the service exists:

```bash
systemctl is-active smbd
systemctl is-enabled smbd
```

`active` means it is running now. `enabled` means it will start after a reboot.

## 3. Create the share directory carefully

Only do this after confirming the mount. The plain `mkdir` below deliberately
stops if the directory already exists; that is safer than recursively changing
an existing folder by accident.

```bash
sudo mkdir /mnt/one/KK_SHARE
sudo chown youruser:youruser /mnt/one/KK_SHARE
sudo chmod u+rwx,go-rwx /mnt/one/KK_SHARE
ls -ld /mnt/one/KK_SHARE
```

On an ext4 filesystem, those ownership and mode changes are straightforward.
On NTFS3, the mount configuration may shape the result instead. Check the final
`ls -ld` output rather than assuming every NTFS mount handles later `chown` and
`chmod` calls in the same way.

## 4. Give Samba an account to authenticate

Samba keeps its own password record. It is separate from the Linux login
password unless a system is deliberately configured to synchronize them.

```bash
sudo smbpasswd -a youruser
sudo smbpasswd -e youruser
sudo pdbedit -L
```

The first command asks for a Samba password. The second enables the account.
`pdbedit -L` confirms that Samba knows about it, but a real connection test
later is still the final proof that the password works.

## 5. Add a small, explicit Samba configuration

Back up the current configuration before editing it:

```bash
sudo cp /etc/samba/smb.conf /etc/samba/smb.conf.bak.$(date +%Y%m%d_%H%M%S)
sudoedit /etc/samba/smb.conf
```

For a fresh standalone server, this is a compact starting point. If the file
already contains shares you need, preserve them and add the new `[KK_SHARE]`
section instead of replacing the whole file.

```ini
[global]
   workgroup = WORKGROUP
   server string = %h Samba server

   # Modern SMB only; old SMB1 and SMB2 clients cannot connect.
   server min protocol = SMB3_00
   disable netbios = yes

   security = user
   ntlm auth = ntlmv2-only

   load printers = no
   disable spoolss = yes

[KK_SHARE]
   comment = Private LAN share
   path = /mnt/one/KK_SHARE
   browseable = yes
   read only = no
   guest ok = no
   valid users = youruser

   # Keep Samba's file operations aligned with the mounted filesystem owner.
   force user = youruser
```

The important lines are deliberately plain:

- `server min protocol = SMB3_00` keeps the server on modern SMB.
- `guest ok = no` means a client must authenticate.
- `valid users = youruser` narrows the share to one Samba account.
- `force user = youruser` is particularly useful when an NTFS mount presents
  files as one Linux owner.

This is a single-user home-network example. A family share, an office, an
Active Directory domain, or access from outside the home deserves a different
identity and security design.

## 6. Validate before restarting Samba

Never make a syntax test depend on whether a service happened to restart.

```bash
sudo testparm -s
sudo systemctl restart smbd
sudo systemctl enable smbd
systemctl is-active smbd
```

`testparm -s` shows the configuration as Samba parsed it. Stop for any error
or unexpected warning. Once it succeeds, restart `smbd` and confirm it is
active.

## 7. Allow SMB from the LAN, not everywhere

First identify the real local subnet. In this example, an address of
`192.168.1.23/24` means that the home LAN is `192.168.1.0/24`.

```bash
ip -4 addr show enp0s3
ip route | grep default
```

Then allow only TCP port 445 from that subnet:

```bash
sudo ufw allow from 192.168.1.0/24 to any port 445 proto tcp
sudo ufw status verbose
```

The `/24` is compact notation for addresses beginning with `192.168.1.`. Your
network may be different. The safety property is the narrow source range, not
the example numbers.

With NetBIOS disabled and SMB3 required, the old 137–139 NetBIOS ports are not
part of this setup. Do not open them unless you have a specific legacy-client
reason and understand the trade-off.

!!! warning "Enabling a firewall is a separate decision"

    If UFW is inactive, do not enable it blindly on a remote machine. Make sure
    the firewall already permits the management access you need, such as SSH,
    before running `sudo ufw enable`.

## 8. Test locally, then from another device

The server can test the same SMB path a client uses:

```bash
smbclient -L //127.0.0.1 -U youruser --option='client min protocol=SMB3_00'
smbclient //127.0.0.1/KK_SHARE -U youruser --option='client min protocol=SMB3_00'
```

The first command lists the available shares. In the interactive second command,
try `ls`, create a harmless directory, then remove it again:

```text
mkdir share-test
rmdir share-test
```

Once this works locally, test from another device on the same LAN:

- **Windows:** open `\\server-ip\KK_SHARE` in File Explorer.
- **macOS:** in Finder, choose **Go → Connect to Server** and enter
  `smb://server-ip/KK_SHARE`.
- **Linux:** use the file manager, `smbclient`, or mount the share with
  `cifs-utils`.

Use the server's current IP address if local DNS or name discovery is not part
of your network. That is less elegant than a hostname, but far easier to
diagnose.

## Adding a second share later

Adding a second folder does not require another firewall rule: Samba already
listens on TCP 445. It does require care with the configuration file.

Do **not** re-run a command that writes the whole `smb.conf` file. Back it up,
then append a new share stanza:

```bash
sudo cp /etc/samba/smb.conf /etc/samba/smb.conf.bak.$(date +%Y%m%d_%H%M%S)

sudo tee -a /etc/samba/smb.conf > /dev/null << 'CONF'

[MM_SHARE]
   comment = Second private LAN share
   path = /mnt/two/MM_SHARE
   browseable = yes
   read only = no
   guest ok = no
   valid users = youruser
   force user = youruser
CONF

sudo testparm -s
sudo systemctl restart smbd
```

The `-a` in `tee -a` means append. The text between `<< 'CONF'` and the final
`CONF` is a here-document, a tidy way to pass several configuration lines to
one command. The quoted marker prevents the shell from expanding anything
inside it.

Create and inspect `/mnt/two/MM_SHARE` first, using the same mount check as the
first share. An absent disk can leave behind an empty-looking mount point, and
that is exactly the kind of problem a little preparation prevents.

## Troubleshooting in a useful order

When a client cannot connect, work from the local system outward:

1. `findmnt -T /mnt/one -o TARGET,SOURCE,FSTYPE,OPTIONS` — is the intended disk
   mounted?
2. `sudo testparm -s` — does Samba accept the configuration?
3. `systemctl is-active smbd` — is the service running?
4. `smbclient -L //127.0.0.1 -U youruser` — does the server work locally?
5. `sudo ufw status numbered` — is TCP 445 limited to, but allowed from, the
   intended LAN?
6. Test another device using the server IP address.

This order separates disk, configuration, service, authentication, and network
problems. That is much quicker than changing several things at once and hoping
one of them helped.

## Keep the reasoning with the commands

The most useful output of this kind of work is not only a working share. It is
a small record of what was checked, why the firewall is narrow, and how to add
the next share without undoing the first one. That turns a one-evening repair
into a configuration you can reuse during a rebuild or adapt for another
machine.

## Sources and further reading

- [Samba documentation](https://www.samba.org/samba/docs/) for server and
  client reference material.
- [Samba `smb.conf(5)`](https://www.samba.org/samba/docs/current/man-html/smb.conf.5.html)
  for configuration settings and their scopes.
- [Linux NTFS3 documentation](https://docs.kernel.org/filesystems/ntfs3.html)
  for mount options and filesystem behavior.
- [Ubuntu firewall documentation](https://documentation.ubuntu.com/server/how-to/security/firewalls/)
  for UFW concepts and examples.

_Reviewed 2026-10-05. Samba packages, local network layouts, and operating
system defaults can change; verify them on the machine being configured._
