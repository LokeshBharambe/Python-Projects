import instaloader 

ig = instaloader.Instaloader() # Creating an Instaloader() object

usrname = input("Enter username:")

profile = instaloader.Profile.from_username(ig.context, usrname)  # Fetching the details 

# Printing details
print("Username: ", profile.username)
print("Number of Posts Uploaded: ", profile.mediacount)
print(profile.username + " has " + str(profile.followers) + " followers.")
print(profile.username + " is following " + str(profile.followees) + " people")
print("Bio: ", profile.biography)

ig.download_profile(usrname, profile_pic_only=True)  # Downloading the profile picture

# Downloading posts
for post in profile.get_posts():
    ig.download_post(post, target=profile.username)
