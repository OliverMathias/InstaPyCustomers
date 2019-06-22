# collect OG followees
# follow and like from hashtags for 5 days
# - follow and like for 8/9 hrs per day
# Day 6 & 7 unfollow but exclude the OG followees

# Command is like This
# >>> Endless_VX.X.py [Excel Row Number]
import sys
import schedule
import time
import json
import glob
import os
from openpyxl import load_workbook
from instapy import InstaPy
from instapy import smart_run

#Setting Control and Accessor Variables
#------------------------------

# Setting up and Accessing the workbook
wb = load_workbook(filename = 'Accounts.xlsx')
sheet_ranges = wb['Sheet1']

# Initializing Variables
insta_username = (sheet_ranges['A' + sys.argv[1]].value)
insta_password = (sheet_ranges['B' + sys.argv[1]].value)

# Follow and Unfollow times
follow_time = (sheet_ranges['K' + sys.argv[1]].value)
unfollow_time = (sheet_ranges['L' + sys.argv[1]].value)

# Sets the number of days the follow/like script should loop.
daysToLoop = (sheet_ranges['E' + sys.argv[1]].value)

# Setting Daily follow ammmt (300 for new accounts, 600 for old accounts)
# if total daily follow is set to 300, it will only follow about 150
# also, it takes ~1 hour for each 100 follow in this var.
total_daily_follow = (sheet_ranges['C' + sys.argv[1]].value)

# A global following list of the people who's accounts to target
follow_list = []
follow_list.append((sheet_ranges['F' + sys.argv[1]].value))
follow_list.append((sheet_ranges['G' + sys.argv[1]].value))
follow_list.append((sheet_ranges['H' + sys.argv[1]].value))

# This pulls a True or False Statement from the Excel sheet and
# it determines the actions of the script based on what they want
skip_business_decicision = (sheet_ranges['I' + sys.argv[1]].value)

# Printing out a kind of 'roadmap' to the console to double check
print()
print()
print('*************************************************************************')
print()
print("Starting Session of: ", daysToLoop, " number of days.")
print("Account Username: ", insta_username)
print("Account Password: ", insta_password)
print("With a Beginning Total Daily Follow of: ", total_daily_follow)
print("And a Following List of: ", follow_list)
print()
print('*************************************************************************')
print()
print()
#------------------------------

def getOGFollowees():
    target_profile = insta_username

    # get an InstaPy session!
    # set headless_browser=True to run InstaPy in the background
    session = InstaPy(username=insta_username,
                      password=insta_password,
                      headless_browser=True)

    session.login()
    # Grab the following list and save it
    ogFolloweesList = session.grab_following(username= target_profile, amount="full", live_match=True, store_locally=True)
    return ogFolloweesList
    session.end()

#@staticmethod
def followSession(self):
    # Global vars
    global total_daily_follow
    global daysToLoop
    # login credentials
    target_profile = insta_username

    # get an InstaPy session!
    # set headless_browser=True to run InstaPy in the background
    session = InstaPy(username=insta_username,
                      password=insta_password,
                      headless_browser=True)
    session.login()


    # Only use Latin Alphabet
    session.set_mandatory_language(enabled=True, character_set='LATIN')


    session.set_relationship_bounds(enabled=True,
                potency_ratio=None,
                delimit_by_numbers=True,
                max_followers=6000,
                max_following=3000,
                min_followers=30,
                min_following=30)

    follow_number_per_account = (total_daily_follow/len(follow_list))
    follow_number_per_account = int(follow_number_per_account)

    # this is the settings for the following below
    session.set_user_interact(amount=2, randomize=True, percentage=20, media='Photo')
    session.set_do_like(enabled=True, percentage=100)
    session.set_do_comment(enabled=False, percentage=35)
    session.set_do_follow(enabled=False, percentage=0)

    # Skip the following types of accounts
    session.set_skip_users(skip_private=True, skip_no_profile_pic=True, skip_business=skip_business_decicision)

    # Quota supervisor so we don't go over instagram's limits
    session.set_quota_supervisor(enabled=True, sleep_after=["likes", "comments_d", "follows", "unfollows", "server_calls_h"], sleepyhead=True, stochastic_flow=True, notify_me=True,
                        peak_likes=(57, 585),
                        peak_comments=(21, 182),
                        peak_follows=(48, None),
                        peak_unfollows=(35, 600),
                        peak_server_calls=(450, None))

    # the real action section
    session.follow_user_followers(follow_list, amount=follow_number_per_account, randomize=True, interact=True, sleep_delay=501)

    session.join_pods()

    # This subtracts a day, each itteration of the 8:00 AM Loop
    # This must be assigned global because it's MODIFYING
    # The global variable (not just calling it)
    daysToLoop -= 1

    # This adds to the daily follow by 15 to 'warm up' the account
    total_daily_follow += 30

    print()
    print("---------------------------------------------")
    print("Total Daily Follow Now: ", total_daily_follow)
    print("Days to Loop: ", daysToLoop)
    print("---------------------------------------------")
    print()
    session.end()


def unfollowSession(self):
    pass
    # Setting global variables
    global ogFolloweesList
    global total_daily_follow
    global daysToLoop

    target_profile = insta_username

    # get an InstaPy session!
    # set headless_browser=True to run InstaPy in the background
    session = InstaPy(username=insta_username,
                      password=insta_password,
                      headless_browser=True)
    #quota supervisor
    session.set_quota_supervisor(enabled=True, peak_server_calls=(490, None), sleep_after=["server_calls_h"], sleepyhead=True)

    session.login()

    try:
        # This pulls the oldest file in the locally saved followees backup list
        path = "./logs/" + insta_username + "/relationship_data/" + insta_username + "/following"
        files = os.listdir(path)
        paths = [os.path.join(path, basename) for basename in files]
        OG_followees_List_Path = min(paths, key=os.path.getctime)

        # This reads in that .json file and makes it a variable
        with open(OG_followees_List_Path) as f:
           hardcoded_followees_data = json.load(f)

        # Combining the lists just in case something messes up
        Master_OG_Followees = []
        Master_OG_Followees.extend(hardcoded_followees_data)
        Master_OG_Followees.extend(ogFolloweesList)

        # This sets the don't include so we don't unfollow our OG friends.
        session.set_dont_include(Master_OG_Followees)

        # the unfollowing section
        session.unfollow_users(amount=(total_daily_follow/2), InstapyFollowed=(True,"all"), style="FIFO", unfollow_after=0, sleep_delay=650)
        session.end()

        # This adds a day, each itteration of the 12:00 PM Loop
        daysToLoop -= 1

        # This adds to the daily follow by 15 to 'warm up' the account
        total_daily_follow += 30

        print()
        print("---------------------------------------------")
        print("Total Daily Unfollow Now: ", total_daily_follow)
        print("Days to Loop: ", daysToLoop)
        print("---------------------------------------------")
        print()

    except:
        print('********************************************************')
        print()
        print("Could not get hardcoded backup, skipping unfollow.")
        print()
        print('********************************************************')


def unfollowAllSession(self):
    pass
    # Setting global variables
    global total_daily_follow
    global daysToLoop

    target_profile = insta_username

    # get an InstaPy session!
    # set headless_browser=True to run InstaPy in the background
    session = InstaPy(username=insta_username,
                      password=insta_password,
                      headless_browser=True)
    #quota supervisor
    session.set_quota_supervisor(enabled=True, peak_server_calls=(490, None), sleep_after=["server_calls_h"], sleepyhead=True)

    session.login()

    try:

        # the unfollowing section
        session.unfollow_users(amount=(total_daily_follow/2), allFollowing=True, style="FIFO", unfollow_after=0, sleep_delay=650)
        session.end()

        # This adds a day, each itteration of the 12:00 PM Loop
        daysToLoop -= 1

        # This adds to the daily follow by 15 to 'warm up' the account
        total_daily_follow += 30

        print()
        print("---------------------------------------------")
        print("Total Daily Unfollow Now: ", total_daily_follow)
        print("Days to Loop: ", daysToLoop)
        print("---------------------------------------------")
        print()

    except:
        print('********************************************************')
        print()
        print("Something went wrong when unfollowing all.")
        print()
        print('********************************************************')


#MAIN
if __name__ == "__main__":

    if (sheet_ranges['J' + sys.argv[1]].value) == "Unfollow All":

        # Resets the number of days to loop to the number of days we followed,
        # Except this time we're gonna be using it for unfollow
        daysToLoop = (sheet_ranges['E' + sys.argv[1]].value)

        # Setting up unfollow sessions
        schedule.every().day.at(unfollow_time).do(unfollowAllSession,'The Unfollow Script is Starting!').tag('unfollow')
        print()
        print("---------------------------------------------")
        print("Strategy: Unfollow All")
        print("Waiting Til: ",unfollow_time)
        print("---------------------------------------------")
        print()
        while daysToLoop > 0:
            # Only checks once per minute so as to minmize CPU Calls
            time.sleep(60)
            schedule.run_pending()

        # Clears the schedule of unfollow tasks
        schedule.clear('unfollow')

        # We're Done!
        print("DONE")

    elif (sheet_ranges['J' + sys.argv[1]].value) == "Unfollow":
        #Gets the OG followees and saves them in a global variable
        # We're adding this blank list in the case that we get to the Master_OG_Followees
        # merge section and we skipped the getOGFollowees method, meaning it would
        # throw an error
        ogFolloweesList = []
        ogFolloweesList.extend(getOGFollowees())

        # Setting up unfollow sessions
        schedule.every().day.at(unfollow_time).do(unfollowSession,'The Unfollow Script is Starting!').tag('unfollow')
        print()
        print("---------------------------------------------")
        print("Strategy: Unfollow")
        print("Waiting Til: ",unfollow_time)
        print("---------------------------------------------")
        print()
        while daysToLoop > 0:
            # Only checks once per minute so as to minmize CPU Calls
            time.sleep(60)
            schedule.run_pending()

        # Clears the schedule of unfollow tasks
        schedule.clear('unfollow')

        # We're Done!
        print("DONE")

    elif (sheet_ranges['J' + sys.argv[1]].value) == "Full":
        #Gets the OG followees and saves them in a global variable
        # We're adding this blank list in the case that we get to the Master_OG_Followees
        # merge section and we skipped the getOGFollowees method, meaning it would
        # throw an error
        ogFolloweesList = []
        ogFolloweesList.extend(getOGFollowees())

        # this schedules the follow by users and like by hashtags for 8 AM every day
        schedule.every().day.at(follow_time).do(followSession,'The Follow & Like Script is Starting!').tag('follow')
        print()
        print("---------------------------------------------")
        print("Strategy: Full")
        print("Waiting Til: ", follow_time)
        print("---------------------------------------------")
        print()
        while daysToLoop > 0:
           # Somehow lowers the CPU usage percentage
           # I think because instead of going at the max speed of the core (Fast as fuck)
           # It only does the loop every 60 seconds
           # every 60 seconds because it WILL trigger at the desired time AND
           # It will only trigger once, so run pending will only have
           # 1 task to run, not 4 backed up ones.
           time.sleep(60)
           schedule.run_pending()

        # Clears the schedule of follow tasks
        schedule.clear('follow')

        # Sleeps for 24 hours
        print("")
        print("Sleeping For 1 Day Between Follow and Unfollow Cycles")
        print("Now is your chance to adjust the number of unfollow days if need be.")
        print("")

        time.sleep(60*60*24)

        # Resets the number of days to loop to the number of days we followed,
        # Except this time we're gonna be using it for unfollow
        daysToLoop = (sheet_ranges['E' + sys.argv[1]].value)

        # Setting up unfollow sessions
        schedule.every().day.at(unfollow_time).do(unfollowSession,'The Unfollow Script is Starting!').tag('unfollow')
        print()
        print("---------------------------------------------")
        print("Waiting Til: ", unfollow_time)
        print("---------------------------------------------")
        print()
        while daysToLoop > 0:
        # Only checks once per minute so as to minmize CPU Calls
          time.sleep(60)
          schedule.run_pending()

        # Clears the schedule of unfollow tasks
        schedule.clear('unfollow')

        # We're Done!
        print("DONE")

    elif (sheet_ranges['J' + sys.argv[1]].value) == "Follow":

            # this schedules the follow by users and like by hashtags for 8 AM every day
            schedule.every().day.at(follow_time).do(followSession,'The Follow & Like Script is Starting!').tag('follow')
            print()
            print("---------------------------------------------")
            print("Strategy: Follow")
            print("Waiting Til: ", follow_time)
            print("---------------------------------------------")
            print()
            while daysToLoop > 0:
               # Somehow lowers the CPU usage percentage
               # I think because instead of going at the max speed of the core (Fast as fuck)
               # It only does the loop every 60 seconds
               # every 60 seconds because it WILL trigger at the desired time AND
               # It will only trigger once, so run pending will only have
               # 1 task to run, not 4 backed up ones.
               time.sleep(60)
               schedule.run_pending()

            # Clears the schedule of follow tasks
            schedule.clear('follow')

            # We're Done!
            print("DONE")

    else:
        print()
        print("Well shit I don't know what to do.")
        print()
