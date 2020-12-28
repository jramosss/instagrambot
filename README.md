# Instagram Bot (With a little bit of scraping)  
 
## Requirements
* Selenium
* Python3
* Chromedriver

If you want to use this poor bot (i dont recommend it) you will need to create a file called `credentials.py`
with 2 variables:  
`username = your_instagram_username` and `password = your_instagram_password`. 
It is important that your variables are called exactly that way (unless you change the import in `instagrambot.py`)
Also you will need to download your [chromedriver](https://chromedriver.chromium.org/) according to your chrome version and change the constant 
`CHROMEDRIVER_ROOT` to your chromedriver root.

### Functions:

* `login` : login with your credentials (from credentials.py), avoiding pop-ups

* `get_fst_photo` : returns the link from the first photo of the given profile

* `comment` : comments `message` in the `post`
  
* `autocomment` : comments a `shortList` burst of comments `n` times in a `post`
  
*  `scroll_and_like`

* `autoscroll` : autoscrolls for `n` time

* `get_followers` returns the list of followers of `who`
