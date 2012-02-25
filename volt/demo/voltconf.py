# Volt configurations file

from os.path import join

from volt.config.base import Config


# Volt configurations
VOLT = Config(

    ###
    # Temp options for development
    CONTENT_DIR = "content_dev",
    TEMPLATE_DIR = "templates_dev",
    SITE_DIR = "site_dev",
    ###

    # Flag for colored terminal output
    COLORED_TEXT = True,
)


# General project configurations
SITE = Config(

    # Your site name
    TITLE = "Volt Demo Site",

    # Your site URL
    URL = "http://127.0.0.1",

    # Your site description
    DESC = "Because static sites have potential",

    # Engines used in generating the site
    # Available engines are 'page', 'blog', and 'collection'
    # To disable an engine, just remove its name from this list
    ENGINES = ['blog', ],
)


# Blog engine configurations
BLOG = Config(
  
    ####
    # Temp options for development
    CONTENT_DIR = join(VOLT.CONTENT_DIR, 'blog'),
    ####

    # URL for all blog content relative to root URL
    URL = "/blog",

    # Blog posts permalink, relative to blog URL
    PERMALINK = "{time:%Y/%m/%d}/{slug}",

    # Blog posts author, can be overwritten in individual blog posts
    AUTHOR = "Admin",

    # The number of displayed posts per pagination page
    POSTS_PER_PAGE = 10, 

    # Default length (in words) of blog post excerpts
    EXCERPT_LENGTH = 50, 
)


# Page engine configurations
PAGE = Config(

    # URL for all page content relative to root URL
    URL = "/page",

    # Page permalink, relative to page URL
    PERMALINK = "{slug}",
)
