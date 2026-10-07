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
  on the system disk today? (It's surprisingly easy to miss this.)
- Which Linux account owns the files, and which Samba account may connect?
- Does the server accept only modern SMB3 clients?
- Is TCP port 445 open only to the home subnet, rather than to every network
  the machine might join?
- How should the firewall rule be written so it allows the intended local
  devices without opening the share more widely?
- Will the configuration still make sense when a second share appears later?

None of these are exotic. They're the exact reasons why a quick one-liner from
a forum can work once and then leave you wondering what assumptions were made.
If you find yourself in that position, it's usually one of those quiet
questions.

The filesystem mattered especially in my case. The example share lives on an
NTFS volume mounted at `/mnt/one`. NTFS and Linux do not represent ownership in
quite the same way, so the mount options decide how Linux presents the files.
That makes the mount the first place to check, before anyone starts repairing
permission problems inside Samba.

!!! note "A useful mental model"

    If something goes wrong later, it's worth remembering the three gates: the disk
    mount (can Linux reach the files?), Samba authentication (which authenticated
    user can ask for them?), and the firewall (which machines can even reach Samba
    on port 445). All three need to line up. A small mismatch in any of them tends
    to produce confusing error messages.

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
availability. The useful contribution was structure rather than length: the
agent separated what was documented, what depended on a particular
configuration, and what was too broad to state as a rule.

### It made the safety boundaries visible

The resulting Samba setup has a few deliberately boring properties:

- SMB3 is the minimum protocol, so SMB1 and SMB2 clients don't connect.
- A named Samba user authenticates; guest access stays off.
- The firewall permits TCP 445 only from the known local subnet.
- Samba's configuration is checked before the service is restarted.
- A local connection test comes before testing from another device.

None of these are flashy. Together, though, they turn "it seems to work" into a
setup whose boundaries are easier to explain later and easier to trust.

### It helped turn a successful command into a maintainable guide

The frustrating part of a one-off fix is that it is easy to forget what was
assumed. The agent helped convert commands into checks, explanations, and
expected outcomes. For example, the guide now distinguishes an unmounted disk
from an empty-looking mount point, and it explains why appending a second share
is safer than re-running the command that rewrites the whole `smb.conf` file.

That is where the real time gain landed. The typing was never the slow part.
The slow part was returning to the same uncertainty: which setting mattered,
what was tested, and whether a convenient shortcut had widened access by
accident.

### A preview failure became a metadata question

One small failure made that method feel practical. Sometimes a file on the
share would report “File preview not available” in macOS Finder or iOS Files,
then preview normally after reconnecting to the server. Because the same file
worked after a reconnect, a fixed file-size limit was not a convincing
explanation. The more useful question was what the client had cached about the
file and what metadata Samba was offering during the next connection.

The inspection found an SMB3-only share on an NTFS3-backed disk, with no Apple
compatibility VFS module configured. Rather than copying a pile of macOS Samba
tweaks, the agent reduced it to a testable sequence: verify that the actual
filesystem can create, read, and remove a small extended attribute; only then
enable Samba's `vfs_fruit` Apple metadata support and its named-stream backend;
validate the configuration before restarting; then reconnect the clients and
repeat the preview. Keeping resource forks in files rather than generic
extended attributes avoids turning a small metadata compatibility fix into a
large-xattr storage assumption.

That does not prove every unavailable preview is a server bug—client session
state and Wi-Fi interruptions still matter. It does turn an intermittent,
vague complaint into a bounded investigation with a clear reason for every
step. The companion guide records the complete, reversible procedure.

## The agent helped me satisfy my curiosity

The agent did far more than suggest the commands for a Samba share. It became a
research partner for the questions that would otherwise have stayed as small,
unsettling doubts: what does NTFS support actually look like in the current
Linux kernel, which Samba security concerns are real for a private LAN, and
which ones are warnings better suited to a public-facing server?

It also helped me compare the alternatives instead of treating Samba as the
default by inertia. NFS remains a good fit in some Linux-first environments,
but its client support and authentication model make it a different trade-off
for a household that includes Windows and macOS. A NAS could solve this problem
too, but for one machine sharing a disk on a trusted home network, it would add
cost and another system to maintain without solving a problem I actually had.

Most importantly, the conversation followed the curiosity behind the setup.
Rather than stopping at “make this folder visible,” it kept asking what each
choice meant: why SMB is still relevant, where the security boundary really
is, how the filesystem affects the share, and what I would be giving up by
choosing a different protocol or appliance. That made the final configuration
feel less like a borrowed recipe and more like a decision I could explain,
maintain, and revisit later.

## The checks I would keep even in a short guide

Three details from the longer setup earned their place because they prevent
very ordinary mistakes.

### Samba has its own password record

The Linux login account and Samba's network-login record are related, but they
are not the same password store. Creating the share account is an explicit
step:

```bash
sudo smbpasswd -a <your-user>
sudo smbpasswd -e <your-user>
sudo pdbedit -L
```

The first command creates or updates Samba's password for `<your-user>`; the second
makes sure the account is enabled. `pdbedit -L` confirms that Samba knows about
the account. If authentication fails later, don't assume a typo; check
that the account is actually enabled. A real connection test is still the best
proof.

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
smbclient -L //127.0.0.1 -U <your-user>
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
data already in front of you: an iPhone, a Windows laptop, or something else.

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
- [Samba `vfs_fruit(8)`](https://www.samba.org/samba/docs/current/man-html/vfs_fruit.8.html)
  for Apple SMB metadata and resource-fork interoperability.
- [Ubuntu's firewall documentation](https://documentation.ubuntu.com/server/how-to/security/firewalls/)
  for UFW concepts and command examples.

_Technical claims and source links were reviewed on 2026-10-07. Network layout,
Samba versions, and operating-system behavior should still be checked against
the machine being configured._
