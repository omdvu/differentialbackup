Update 2.0:
Added the functionality to do mirror backups, the backup pendrive will be backed up to another pendrive before actually running the differential backup, maintaining 3 versions of the same file.
Also added error file logs, that showcases if any files were missed, in the logs folder

To run it:
docker run -d -v /source/path:/server -v /destination/path:/backup -v /mirror/path:/mirror -v /logs/path:/logs --name containername imagename

Update 1.0:

Hey admin,
This is a very basic backup tool that lets you create a differental copy of your mentioned directory into a mentioned mounted directory(you will have to manually mount it) and also write logs.

Firstly, to build the image:
docker build -t imagename .

Then to run it:
docker run -d -v /source/path:/server -v /destination/path:/backup -v /logs/path:/logs --name containername imagename

In this code, you only change the directory names of your actual locations, and dont change the paths after the colon(:), they are for container use, you can have any containername and imagename.
This is a differential backup, hence, it will copy those files which are new or which have been updated from their previous version found on the backup folder, it avoids special files like sockets, fifos, which are not even considered to be files. Hence, such files may even break the backup system, as this is not a fully professional tool, so if you find any issue, mail me at omprajapatidv@gmail.com, or any suggestions.

This backup every 24 hours, if you want to override that, you can manually run containers every x period of time to run it.

Also, backup time depends on how big are your actual files, and hence it requires you to wait patiently, as well as if the destination mounted device has ample space.

And /logs/path will be the folder on your system that will display the files inside a txt file for both your server and mount.

How to mount? Well actually mounting is as simple as using an external block device. But you have to especially mention it in systems like Linux to mount them, but in other OSs, you will automatically see the folder path, which you use as /destination/path.
Well to mount, you firstly insert the pendrive into your system. You run: lsblk -f, this command will display all your block devices, be it internal or external, usually they are all different according to your partitions, but a trick to find your pendrive will be to check lsblk -f, without inserting the pendrive, and then insert it and again run lsblk -f, the new sd(a-z) you see will be your pendrive.
But your pendrive may have multiple partitions like sdc1 sdc2 sdc3 sdc4, some would be system partitions, you need to find actual storage partition in it, usually it has sizes written, the one with the size of your pendrive is the one you want.
To mount:(run as sudo, it wont work otherwise, or it may if you have changed sudo settings, but please run as sudo)
sudo mount /dev/sdXY /destination/path

Here, /dev is the constant, and /sdXY is the device partition you need to find, and /destination/path is the mount point you want, so in short, the /destination/path will be the path from where you access the pendrive, and that same path needs to be in the run command, as shown above.

You can also backup certain specific folders, example, in your downloads folder, you want to backup the 'photos' folder, and your pendrive mount was at /pendrive(for Linux), or your pendrive may be already showcased if you use UI based OSs, so you run it as:
docker run -d -v /Downloads/photos:/server -v /pendrive:/backup -v /logs:/logs --name backup-photos imagename

This keeps backing up your photos folder every 24hrs, if you want it to backup once, then let the backup run once, you can check if the backup is completed by doing:
docker logs backup-photos, it will display if the backup is done, maybe sometimes it doesn't, but still you can manually check in the folder if your desired files are copied. Once its done, you can stop the container.

A special note for my Linux users, run this with sudo rights, or as root, so it can copy files and paste them without any permission error.

If you face any issue, I'll be happy to help, omprajapatidv@gmail.com, abhimaradiya63@gmail.com.

Regards,
Om, Abhi
