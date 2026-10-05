---
title: Samba Is Still Relevant, and an Agent Helped Me Treat It Seriously
description: A field note on setting up a modern LAN Samba share, the small admin traps around it, and where an AI agent genuinely helped.
keywords:
  - Samba
  - SMB3
  - Linux administration
  - home network
  - AI agents
  - file sharing
icon: lucide/server
---

There is a particular kind of home-network problem that feels too small to
deserve a project until it steals an evening: a useful folder lives on one
Linux machine, while the people and devices that need it use Windows, macOS,
and Linux. Copying files with a USB disk works until it does not. Cloud storage
is convenient until the files are large, private, or simply already sitting on
the local network.

I wanted one ordinary folder, `KK_SHARE`, to be reachable from the machines in
my home without making the rest of the network more complicated. Samba was the
practical choice: it speaks SMB3 over the local network.

One thing I realised again was how many systems a careful share touches: the
disk mount, Linux permissions, the Samba account database, the firewall, and
the client devices. An AI coding agent was useful as a patient second set of
eyes while I researched and documented those layers.

Readers who want the full command-by-command version can jump straight to the
[Samba folder-share guide](../../Linux/samba-folder-share-guide.md).

## Why Samba still earns its place

Samba is the Linux implementation of SMB, the file-sharing protocol built into
Windows and supported by modern macOS and Linux clients. That makes it a very
good answer to a mixed-device household: no additional client application, no
vendor account, and no need to teach every device a different sharing method.

The goal is pleasantly modest. A directory such as `/mnt/one/KK_SHARE` becomes
`\\server\KK_SHARE` on the network. A Windows laptop can open it in Explorer,
a Mac can use Finder, and another Linux machine can mount it when that is
useful. The data stays local, so a large copy travels across the LAN instead of
waiting for an upload and download through somebody else's server.

That is the time saving that matters to me. The first setup needs care; after
that, the folder is simply where the folder is supposed to be. The same share
works from the machines already in the house, and a rebuild has a documented
path back to the same result.

## The small request with several hidden layers

The initial request sounds like one line: "share this folder in my network",
but in practice, it contains a handful of quieter questions:

- Is the data disk actually mounted, or is `/mnt/one` only an empty directory
  on the system disk today?
- Which Linux account owns the files, and which Samba account may connect?
- Does the server accept only modern SMB3 clients?
- Is TCP port 445 open only to the home subnet, rather than to every network
  the machine might join?
- How should the firewall rule be written so it allows the intended local
  devices without opening the share more widely?
- Will the configuration still make sense when a second share appears later?

None of these questions is exotic. They are exactly why a quick command copied
from a forum post can be frustrating: it may create a share that works once,
but leaves its assumptions invisible.

The filesystem mattered especially in my case. The example share lives on an
NTFS volume mounted at `/mnt/one`. NTFS and Linux do not represent ownership in
quite the same way, so the mount options decide how Linux presents the files.
That is not a reason to avoid Samba. It is a reason to check the mount before
trying to repair a permission problem in Samba.

!!! note "A useful mental model"

    Think of the setup as three gates. The disk mount decides whether Linux can
    reach the files. Samba decides which authenticated network user may ask for
    them. The firewall decides which machines are allowed to ask at all. A
    share works only when all three agree.

## Where the agent was actually helpful

The agent's most useful contribution was research discipline. It could look up
the current Samba, Linux-kernel, and firewall documentation while keeping the
question narrow: what does this setting mean on this kind of machine, and what
is the least surprising safe default?

That changed the quality of the work in a few concrete ways.

### It challenged plausible-but-wrong explanations

Some claims sound right because they are repeated often. A good example is the
idea that an NFS server must always export the root of a filesystem rather than
a subdirectory. The real answer is more useful: subdirectory exports are
supported, but the security trade-offs need an explicit decision. That is a
better lesson than replacing one slogan with another.

The same happened with cloud-init, macOS NFS behavior, and Windows NFS
availability. The agent did not merely make the guide longer. It separated
what was documented, what depended on a particular configuration, and what was
too broad to state as a rule.

### It made the safety boundaries visible

The resulting Samba setup has a few deliberately boring properties:

- SMB3 is the minimum protocol, so SMB1 and SMB2 clients do not connect.
- A named Samba user authenticates; guest access stays off.
- The firewall permits TCP 445 only from the local subnet, such as
  `192.168.1.0/24`.
- Samba's configuration is checked before the service is restarted.
- A local connection test comes before testing from another device.

None of these is clever. Together, they turn "it seems to work" into a setup
whose boundaries are easy to explain later.

### It helped turn a successful command into a maintainable guide

The frustrating part of a one-off fix is that it is easy to forget what was
assumed. The agent helped convert commands into checks, explanations, and
expected outcomes. For example, the guide now distinguishes an unmounted disk
from an empty-looking mount point, and it explains why appending a second share
is safer than re-running the command that rewrites the whole `smb.conf` file.

That is where the real time gain landed. Not in typing fewer commands, but in
spending less time returning to the same uncertainty: which setting mattered,
what was tested, and whether a convenient shortcut had widened access by
accident.

## Three small commands that made the setup feel solid

The finished configuration was not complicated. What impressed me was how much
confidence came from asking each command one clear question.

### First, check the disk rather than trusting the directory

An empty mount point can still look perfectly normal. If the data disk is not
mounted, creating a directory under `/mnt/two` creates it on the system disk
instead. This command makes that mistake visible:

```bash
findmnt -T /mnt/two -o TARGET,SOURCE,FSTYPE,OPTIONS
```

For the intended setup, `TARGET` should be exactly `/mnt/two`, and the source
and filesystem type should be the expected disk and `ntfs3`. If the command
reports `/` instead, that is not a Samba problem yet. The disk has not been
mounted where the share expects it.

### Then, let the local network in and nobody else

The firewall rule is deliberately narrow. It permits SMB's TCP port 445 from
the home subnet, `192.168.1.0/24`, and nowhere else:

```bash
sudo ufw allow from 192.168.1.0/24 to any port 445 proto tcp
sudo ufw status verbose
```

`/24` is compact network notation for the addresses beginning with
`192.168.1.`. It is only an example: the right subnet comes from the machine's
own network settings. The important part is the shape of the rule: permit the
known LAN, rather than opening the service to any network the machine happens
to reach.

### Finally, add a share without erasing the first one

This was the command that made me slow down. The first version of `smb.conf`
was written with `tee`, which replaces a file. That is useful once, but
re-running it later would quietly remove the existing share. For a second
share, I backed up the configuration and used `tee -a`; the `-a` means append.

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

   # NTFS3 presents this disk as youruser, so Samba performs file work as youruser too.
   force user = youruser
CONF

sudo testparm -s
sudo systemctl restart smbd
```

The text between `<< 'CONF'` and the final `CONF` is a here-document: a tidy
way to pass several lines to one command. The quoted marker keeps the shell
from expanding anything inside it. The result is easy to read, easy to back up,
and—most importantly—does not pretend that adding a second share is the same
as rebuilding the whole configuration from scratch.

!!! warning "Use your own names and network"

    `MM_SHARE`, `youruser`, `/mnt/two`, and `192.168.1.0/24` describe this example,
    not a universal recipe. Check the mount, user, path, and subnet on the
    actual machine before copying a command.

The companion [Samba folder-share guide](../../Linux/samba-folder-share-guide.md)
walks through the complete setup, validation, client tests, and troubleshooting
sequence.

## The checks I would keep even in a short guide

Three details from the longer setup earned their place because they prevent
very ordinary mistakes.

### Samba has its own password record

The Linux login account and Samba's network-login record are related, but they
are not the same password store. Creating the share account is an explicit
step:

```bash
sudo smbpasswd -a youruser
sudo smbpasswd -e youruser
sudo pdbedit -L
```

The first command creates or updates Samba's password for `youruser`; the second
makes sure the account is enabled. `pdbedit -L` confirms that Samba knows about
the account, but a real connection test is still the final proof that the
password works.

### Say clearly which SMB clients are welcome

The configuration's global section sets the protocol floor once for every
share:

```ini
[global]
   server min protocol = SMB3_00
   disable netbios = yes
```

That means this machine speaks modern SMB3 directly over TCP 445. It leaves out
the older NetBIOS discovery service and the legacy ports that went with it. A
very old client may need a different plan, but keeping that exception out of a
normal home share is easier to reason about.

### Make the configuration prove itself

Restarting a service is not a test. First ask Samba to parse the configuration,
then restart it, then connect to the actual share:

```bash
sudo testparm -s
sudo systemctl restart smbd
smbclient -L //127.0.0.1 -U youruser
```

`testparm -s` reports the configuration as Samba understands it and catches
spelling or syntax mistakes before they become a service outage. The local
`smbclient` check removes Wi-Fi, DNS, and firewall variables from the first
test. Only after that is it time to try another laptop and create, then remove,
a harmless file.

## What the agent did not decide

An agent can research documentation, notice an overconfident claim, and help
write a testable plan. It cannot decide which devices belong on a trusted home
network, whether the shared data is appropriate for every household account,
or whether a firewall exception matches the actual network.

Those are administrator decisions. So is the final check: connect from a real
client, create and remove a harmless test file, and confirm that the share is
both usable and limited to the intended people.

That division of work felt healthy. The machine remained understandable; the
agent reduced the amount of guesswork around it.

## A practical shape for a small home share

For a simple private share, my recommendation is intentionally conservative:

1. Confirm the data disk is mounted at the expected path.
2. Use one known Linux account and a matching Samba password.
3. Require SMB3 and disable guest access.
4. Allow only the home subnet through the firewall.
5. Validate the configuration, restart Samba, and test locally and from a
   second device.
6. Keep the final configuration and its reasoning somewhere you will find
   during the next rebuild.

This is not a one-size-fits-all recipe. A family share with several users, an
office network, an Active Directory domain, or access from outside the home
deserves a different conversation about identity and security. But when a
handful of known devices on one LAN need to reach one folder, boring is exactly
the point: fewer surprises, a smaller exposure, and a setup you can still
explain six months later.

## The durable lesson

Samba earns its place because so much of everyday computing still happens on a
local network. Files move between the machines already on a desk, a shelf, or a
sofa. The useful question is simply whether it fits the people, devices, and
data already in front of you either on an IPhone, a windows laptop or something
else.

For this job, it did. The share made a large local folder practical across
different operating systems. The agent made the process less lonely: it helped
research the corners, challenge shaky assumptions, and leave behind a guide
that explains why the configuration is shaped the way it is.

## In memory of Steve French

While researching this article, I came across the Samba team's memorial for
[Steve French](https://www.samba.org/), who died on August 22, 2026. The team
remembers both his long contribution to the SMB community and the generosity
with which he encouraged others. His work can also be found on
[GitHub](https://github.com/smfrench).

There is something fitting about that being visible on Samba's front page. A
small home share can feel like an ordinary piece of infrastructure, but it
rests on decades of patient work by people who cared enough to make computers
from different worlds talk to one another. Peace to you, Steve.

For the commands and the reasoning behind them, see the companion
[Samba folder-share guide](../../Linux/samba-folder-share-guide.md).

## Sources and further reading

- [Samba documentation](https://www.samba.org/samba/docs/) for the server,
  configuration, and client reference material.
- [Samba `smb.conf(5)`](https://www.samba.org/samba/docs/current/man-html/smb.conf.5.html)
  for the meaning and scope of configuration settings.
- [Linux NTFS3 documentation](https://docs.kernel.org/filesystems/ntfs3.html)
  for the mount options that shape how NTFS permissions appear on Linux.
- [Ubuntu's firewall documentation](https://documentation.ubuntu.com/server/how-to/security/firewalls/)
  for UFW concepts and command examples.

_Technical claims and source links were reviewed on 2026-10-05. Network layout,
Samba versions, and operating-system behavior should still be checked against
the machine being configured._
