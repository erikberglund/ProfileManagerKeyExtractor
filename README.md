## ProfileManagerKeyExtractor

Script to extract payload information from the Profile Manager source code.

**NOTE: This script does not currently handle all payload keys and value types**

I've written this script to test the possibility of extracting all payload information directly from a Profile Manager installation, to circumvent having to create and export profiles from the GUI to see all keys that Profile Manager can include in a profile.

The test was mostly successful, but there are still work that needs to be done to the parsing on the more complex structures, like payloads which take a single or nested dicts, or an array of dicts for example.

I've writte a blog post about the Profile Manager code sctructure and this script here: [Extracting Payload Keys From Profile Manager]()