from crate.theme.rtd.conf.cloud import *

# Disable version chooser.
html_context.update({
    "display_version": False,
    "current_version": None,
    "versions": [],
})

linkcheck_ignore = [
    "https://eks1.eu-west-1.aws.cratedb.cloud",
    "https://eastus2.azure.cratedb.cloud/",
    "https://portal.azure.com/",
    "https://azuremarketplace.microsoft.com/",
]

linkcheck_timeout = 5
