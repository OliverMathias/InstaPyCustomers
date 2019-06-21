# InstaPyScaled
An Implementation of Tim Grossman's InstaPy That Simplifies Growth, and Tracking of Multiple Accounts Simultaneously

<a href="https://github.com/SeleniumHQ/selenium">
      <img src="https://img.shields.io/badge/built%20with-InstaPy-pink.svg" />
    </a>
    <a href="https://www.python.org/">
    	<img src="https://img.shields.io/badge/built%20with-Python3-red.svg" />
    </a>
    <a href="https://www.python.org/">
      <img src="https://img.shields.io/badge/License-GNU-green.svg" />
    </a>

## General info
This implementation of [InstaPy](https://github.com/timgrossmann/InstaPy) by Tim Grossman improves users' abilities to grow multiple Instagram accounts simultaneously by creating a system where account growing strategies and algorithm choices are kept in a master database

## 🚩 Table of contents
* [General info](#general-info)
* [Problem](#sample)
* [Solution](#flowchart)
* [Flowchart](#flowchart)
* [Excel Variables](#excel-variables)
* [Setup](#setup)
  * [Clone Repository](#clone-repository)
  * [Install ProxyChrome Dependencies](#install-proxychrome-dependencies)
  * [Overwrite ChromeDriver](#overwrite-chromedriver)
  * [Run ProxyChrome](#run-proxychrome)
* [Uses](#uses)
  * [ProxyPrinter](#ProxyPrinter)
* [Acknowledgments](#acknowledgments)
* [License](#license)

## Problem
InstaPy is an amazing tool that allows people to grow their Instagram accounts orders of magnitude faster than normal. However, when trying to grow multiple accounts at once, a user's server or workstation can become incredibly crowded and disorganized.

With multiple instances running at once and it can be hard to modify code in between launches, test optimal configurations, and save successful settings in case of server crash or power outage.

![](http://g.recordit.co/SAklhO5mDT.gif)

## Solution
InstaPyScaled is a python program that uses InstaPy's methods and functions to create a scalable Instagram growth manager. Instead of taking commands directly from the terminal, this InstaPy script pulls information from a Microsoft Excel worksheet. Meaning that all your accounts' data is recorded and stored in one place, making a shift in strategies, start times, or analysis of effectiveness extremely simple.

This also allows for the 'cold storage' of InstaPy settings, meaning a frozen Digital Ocean server, or a power outage won't completely derail the growth of your Instagram Accounts.

![](http://g.recordit.co/tMJeuALX4m.gif)

## Flowchart
![Flowchart](./images//ProxyChromeFlowChart.png)

## Excel Variables
#### Daily Target - Integer
![](images/dailytarget.jpg)

The 'Starting Daily Target' variable in the excel sheet sets the maximum number of users InstaPy will attempt to follow in a single period. While there are hardcoded limits inside the code, they are defined by hourly follow, like, and unfollow numbers. The 'Starting Daily Target' variable is the only way to set the maximum number of Instagram accounts to interact with.

Also, to improve the follower outcome of this program, the 'Starting Daily Target' is increase by 30 each day. So try to set the 'Starting Daily Target' a bit lower for the first day to allow for growth and subsequent efficient unfollowing.

**Note**, there is currently no support from InstaPy for dynamic tallying of valid accounts processed. That is, when an account in the list is analyzed and skipped, for example, because settings specify NO BUSINESS ACCOUNTS, the number of accounts processed counting towards the 'Starting Daily Target' is still incremented.

#### Target Accounts - String
![](images/targetaccount.jpg)

The 3 'Target Account' columns allow the user to specify which accounts the InstaPy follow method should interact with. More specifically, the methods interact with these account's **followers**. In more detail, the code takes the 'Starting Daily Target' variable, floor-divides it by 3 and interacts with that number of followers of each 'Target Account'.

The exact actions taken by the program will be covered in the [Strategy](#strategy---string) section.

#### Skip Business Accounts - Boolean
![](images/skipbiz.jpg)

The 'Skip Business Accounts' variable is a boolean value that tells the program whether to skip accounts identified as Instagram business accounts.

**Note**, make sure the text in this excel column is either 'TRUE' or 'FALSE' in **ALL CAPS** ;)

#### Strategy - String
* ##### Full
* ##### Unfollow
  Make sure to add support for dynamic paths of log files
* ##### Unfollow All
* ##### Follow

#### Follow Start Time - String
![](images/followtime.jpg)

The 'Follow Start Time' variable allows users to set when the program begins its follow and like routine for the 'Follow' and 'Full' strategies. It is very important for account interaction to set the start time early enough that the users will open the Instagram follow/like notification, but not too early that they will still be sleeping.

**Note**, make sure to take into account when the program will finish interacting with the 'Starting Daily Target' amount. Each 100 users added to the 'Starting Daily Target' variable takes ~1 hr to finish interacting with. Also, all times are in military time.

#### Unfollow Start Time - String
![](images/unfollowtime.jpg)

The 'Unfollow Start Time' variable allows users to set when the program begins its unfollow routine for all strategies. It is very important for follower preservation to set the start time late enough that the users will **NOT** open Instagram to see that you have unfollowed.

**Note**, make sure to take into account when the program will finish interacting with the 'Starting Daily Target' amount. Each 100 users added to the 'Starting Daily Target' variable takes ~1 hr to finish interacting with. Also, all times are in military time.

## Dependencies
* python 3.7
* schedule
* glob
* json
* openpyxl
* InstaPy
* Microsoft Excel (or Libre Office)
* [Google Chrome 75.0.37](https://www.google.com/chrome/)
* [Chrome Driver 74.0.37](https://sites.google.com/a/chromium.org/chromedriver/)

#### **Make sure to Download [Compatible](http://chromedriver.chromium.org/downloads/version-selection) Versions of Chrome Driver and Chrome**


## 💾 Setup
#### Clone Repository
Either download from a GUI or run the 'git clone' command on this url...
```
https://github.com/OliverMathias/InstaPyScaled
```

#### Install ProxyChrome Dependencies
cd into the ProxyChrome folder and run this command to install all dependencies at once...
```
$ pip install -r dependencies.txt
```
#### Overwrite ChromeDriver
Make sure to copy your 'chromedriver' file into the ProxyChrome folder...

![](http://g.recordit.co/rcMJLz2inT.gif)

#### Run ProxyChrome
Finally, cd into the folder and run ProxyChrome...
```
$ python ProxyChrome.py
```
Browse anonymously WHILE planting trees!
:seedling: :evergreen_tree: :deciduous_tree:

## Uses
In addition to opening an anonymous chrome window, below are some alternate uses:

#### ProxyPrinter
Included in the code is a method that prints out a list of all the elite level anonymous proxies from [Proxy-List](https://www.proxy-list.download)'s API.
To use this functionality, simple comment out the main method and call the **getProxies()** method like so:

```
if __name__ == "__main__":
    #main()
    getProxies()
```

## Acknowledgments
* [InstaPy](https://github.com/timgrossmann/InstaPy)


## 📜 License
This project is licensed under the GNU License - see the [LICENSE.md](LICENSE.md) file for details
