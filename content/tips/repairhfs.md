---
title: How to repair a TimeMachine Backup Disk that is not detected?
Tags: tech, tips, macos, timemachine
Date: 2021-01-05 12:10
summary: A defect HFS-Partition can lead to the disk not being detected. I show a quick fix to this problem. 
---

So yesterday I tried to make a backup to my time machine volume on an external drive. But strangely while the other Partition showed up normally in my finder, the Time Machine Backup did not. Even with the help of Disk Utility, I was not able to activate it. And repairing this drive also just yielded errors. So I what to do? 


So this a quick guide for you: 

1. Let's check that all cables are fully connected and your external drive is plugged in (if needed)
2. Try to repair the drive/partition with the Disk Utility tool
3. So let us find out, what the error is. Open a Terminal (Applications > Utilities) and type in `DiskUtil list` find the disk that has the problem and note the Identifier for the disk (i.e. /dev/disk2s3). 
4. If it is an HFS drive, try to repair it with `sudo fsck_hfs /dev/rdisk2s3`. You will need to type in your password (it will not be shown)
5. If you get an error about invalid content in Journal try deactivating the journal with `sudo /System/Library/Filesystems/hfs.fs/Contents/Resources/hfs.util -N /dev/disk5s2`
Make sure to use the correct Identifier for your disk.
6. You should be good to go, but go back to the Disk Utility and click on First Aid (on the correct disk). This can take a while depending on the disk size. 
7. You can also turn Journaling back on with `sudo /System/Library/Filesystems/hfs.fs/Contents/Resources/hfs.util -J /dev/disk5s2` in the terminal


## Why did this error happen?
The filesystem often used for external drives on macOS is called HFS and it is a [Journaling File System](https://en.wikipedia.org/wiki/Journaling_file_system), which means it keeps track of operations it still has to do to make sure your data is not corrupted. But this also means if the Journal ever gets corrupted e.g. by powering it off without ejecting, that you cannot activate it. 
