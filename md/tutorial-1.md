# Tutorial 1 - Installing Jason

This tutorial describes how to install everything needed for Jason development, including Java SE, Jason, Eclipse, and the Jason plugin for Eclipse.

<!-- TOC -->

## Java

### Step 1 - Download and install Java SE

Java Platform, Standard Edition (Java SE) is available to download from [Oracle](https://www.oracle.com/java/technologies/java-se-glance.html).

As of February 2024, the latest version is **Java SE 21**.

Select **Download** under this version and then identify the appropriate package for your platform (e.g. **x64 Installer** for Windows).

Download and install the selected package.

## Jason

### Step 2 - Download and install Jason

Jason is available to download from [SourceForge](https://sourceforge.net/projects/jason/files/jason/).

As of February 2024, the latest version is Jason 3.2. However, for this tutorial series we will use **Jason 2.6.3**.

> **Note:** Jason 3.0 introduced some changes to the Jason language that do not guarantee compatibility with this tutorial series so you **must** use Jason 2.6.3.

Download and extract `jason-2.6.3.zip` as a directory called `jason-2.6.3` and remember its absolute path, e.g. `/path/to/jason-2.6.3/`.

> **Note**: Do not install Jason in a protected directory, which includes `/Users/your_username/Downloads/` on macOS.

### Step 3 - Run the Jason configuration tool

Run the file `jason-2.6.3/libs/jason-2.6.3.jar`.

> **Note:** On macOS you may see an error message *"jason-2.6.3.jar" cannot be opened because it is from an unidentified developer*. If this occurs, you should navigate in macOS to **System Preferences > Security & Privacy > General** and select **Open Anyway** beside the message *"jason-2.6.3.jar" was blocked from use because it is not from an identified developer*.

![Figure](figures/jason-setup.png)

Typically most fields are filled automatically, but in some cases you may be required to manually enter values.

Ensure that the following fields are filled and correct:

- **Jason > jason.jar location**: `/path/to/jason-2.6.3/libs/jason-2.6.3.jar`
- **Java Home > Directory**: path to your Java home directory (e.g. `/Library/Java/JavaVirtualMachines/jdk-19.jdk/Contents/Home/` on macOS)
- **Ant libs > Directory**: `/path/to/jason-2.6.3/libs/`
- **JADE > jade.jar location**: `/path/to/jason-2.6.3/libs/jade-4.3.jar`

Select **Save configuration and Exit**.

## Eclipse

### Step 4 - Download and install Eclipse

Eclipse is available to download from [Eclipse Foundation](https://www.eclipse.org/downloads/packages/).

As of February 2024, the latest version is **Eclipse 2023-12**.

Identify the appropriate **Eclipse Installer** package for your platform (e.g. **x86_64** on Windows).

Download and run **Eclipse Installer**.

![Figure](figures/eclipse-install-standard.png)

When prompted, choose **Eclipse IDE for Java Developers**.

![Figure](figures/eclipse-jdk.png).

Ensure that the newly installed version of Java SE is selected and choose an appropriate installation directory.

> **Note**: Do not install Eclipse in a protected directory, which includes `/Users/your_username/Downloads/` on macOS.

Select **Install** to complete the installation.

> **Note:** If you are asked during installation whether to trust unsigned content, choose **Select All** and then **Trust Selected**.

### Step 5 - Install the Jason plugin for Eclipse

Open Eclipse.

![Figure](figures/jason-plugin-install-0.png)

Choose a directory for your workspace and select **Launch**.

![Figure](figures/jason-plugin-install-0b.png)

Select **Help > Install New Software > Add**.

Select **Add...** in the new window.

In the **Name** field enter `jasonide` and in the **Location** field enter the following URL:

`https://seis.bristol.ac.uk/~km17304/jasonide_feature/`

![Figure](figures/jason-plugin-install-1.png)

Select **Add**.

![Figure](figures/jason-plugin-install-2.png)

Unmark the checkbox labelled **Group items by category**.

![Figure](figures/jason-plugin-install-2b.png)

Mark the checkbox beside **Jasonide_feature** and select **Next**.

![Figure](figures/jason-plugin-install-3.png)

Select **Next** again.

![Figure](figures/jason-plugin-install-4.png)

Accept the terms and select **Finish**.

> **Note:** If you are asked during installation whether to trust unsigned content, choose **Select All** and then **Trust Selected**.

![Figure](figures/jason-plugin-install-6.png)

Select **Restart Now**.

Eclipse should now be open and ready for Jason development.

## Test that it works

### Step 6 - Create a new Jason project

Select **File > New > Other > Jason > Jason Project** from the Eclipse menu.

![Figure](figures/new-jason-project-1.png)

Select **Next**.

![Figure](figures/new-jason-project-2.png)

Enter `hello_world` in the **Project name** field and select **Finish**.

![Figure](figures/new-jason-project-3.png)

If you are prompted to open the project in **Jason perspective**, select **Open Perspective**.

A new Jason project will be created with a default directory structure and two auto-generated files: `src/asl/sample_agent.asl` and `hello_world.mas2j`.

> **Note:** To see the new Jason project you may need to close the **Welcome** tab.

### Step 7 - Run the Jason project

With the **hello_world** project in focus, select **Run Jason Application** in the Eclipse toolbar.

> **Note:** There may be two identical buttons in the Eclipse toolbar; ensure that you select the button labelled **Run Jason Application** rather than the button labelled **Run**.

![Figure](figures/run-hello-world.png)

The above window should appear, which confirms that Jason is working correctly.

### Step 8 - Terminate the Jason project

Select **Stop** at the bottom of the window.

## Conclusion

You should now have a working installation of Jason ready to use for the rest of this tutorial series.

If you encountered issues during the installation and have been unable to resolve them yourself, please contact Kevin McAreavey via email or speak to a teaching assistant during one of the lab sessions.
