# C2toDS-Refresh
An attempt to bugfix and polish Moe's C2toDS, with an emphasis on instinct-friendliness and navigability.

# Development Goals

* Priority One is to bring the metaroom up to current [development standards](https://docs.google.com/spreadsheets/d/1CHKnTzjdAJap-tcMcpKPR5NMYvmmpRYZZUxLJo453-c/edit#gid=1354565364) and ensure that it isn't overwhelmingly unfair to creatures. This includes ensuring that all agents have proper scripts/stims and that CA links and transportation methods allow creatures full access to the world's many splendors.
* Ecology fixes and adding missing content are also on the radar, but will receive more attention once the room is more instinct-friendly.

# How To Help Out

* Submit issues! Submit bugs, concerns, ideas, feature requests, and anything else related to the project. You can also browse the existing issues and contribute to the discussions therein.
* Help fill out the Agent Help Descriptions for the catalogue files! Many of them are currently very short or consist only of the agent names. You can find the url to the editable spreadsheet in C2toDS Classifiers.csv.
* Contribute fixes! If you're new to Github and don't want to dig deeply into the mess that is git, there's a brief video walkthrough of how to contribute [here](https://youtu.be/O7GV_Fdk8pY).
* Please make sure any new agents use the C2toDS classifier range (50200 - 50299).

# How To Set Up

There isn't a finished release for this yet, but you're welcome to download, test, and develop the files.

## The Recommended Way
This will automatically inject C2toDS into every world you make until you remove the Bootstrap Folder, but is the easiest way to edit and update the cosfiles as you go along.
* Download (Code > Download as zip) and extract the files.
* Rename the dev/Scripts folder to something like "015 C2toDS" and place it in your Docking Station/Bootstrap folder. When you are tired of testing, you can move or remove this folder to stop injecting C2toDS in all your worlds,
* Place the contents of dev/Sounds into your Docking Station/Sounds folder, the contents of dev/Images into your Docking Station/Images folder, and so on with the rest of the folders.
* Start a new world! You can teleport to C2toDS by using the teleporter in the workshop.
* **Don't open any worlds that you don't want C2toDS injected into** until you have removed the C2toDS folder from your Bootstrap.
* Remember to check back and re-download for the latest updates!

## The Alternative Way
This way is not well-tested. It involves compiling the files into a single injectable agent. It requires the use of Python and [Monk](https://creatures.wiki/Jagent). Keep in mind that injecting such a large agent will freeze your game for several seconds (and may even crash it).
* Download (Code > Download as zip) and extract the files.
* Run compiler.py and follow the directions that it gives you.
* After compiling the agent, you can move the agent into your My Agents folder and delete the compile folder.
* Note you may need to manually move the c2tods.mng from the Sounds folder into your game's Sounds folder anyway, since MNGs don't often extract properly.
* Remember to re-compile the agent whenever there are updates to make sure you're running the latest version!

## The Really Slow Way
If you really want, after moving all the assets into their proper folders, you can use the CAOS tool to inject each cos file individually into the game. Make sure you inject them in numerical order. Useful if you want to leave some files out.



# Links 

https://discordapp.com/invite/zRR8PdT - The CAOS Coding Cave Discord (Development discussion in #C2toDS-Refresh)

https://creatures2todockingstation.blogspot.com/ - Moe's original C2toDS development blog and download.

https://creaturescaves.com/forum.php?view=12&thread=7208 - The thread that inspired this refresh! Wherein Moe states:
>  I never finished C2toDS and likely never will. It’s about 85-90% complete, but there are a few missing machines and some bugs floating about (sometimes literally… those wasps omg…and lordy the frogs!). If someone wanted to step in and fix some bugs or add in the last of the content, go for it!
