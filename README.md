# This script was just an early test and proof of concept. @mosen has written a real tool for this now, please check that out instead: https://github.com/mosen/profiledocs

## ProfileManagerKeyExtractor

Script to extract payload information from the Profile Manager source code.

## Disclaimer
 **This script is currently just a proof of concept, NOT a finished tool.**  
 **Many of the regexes and python implementations are not refined, just the first I could think of to do the job.**

## Description

Here's a link to my companion blog post for this script: [Extracting Payload Keys From Profile Manager](http://erikberglund.github.io/2016/Extracting_Payload_Keys_From_Profile_Manager/) 

I've written this script to test the possibility of extracting payload information directly from a Profile Manager installation to circumvent having to create and export profiles from the GUI in order to find the keys Profile Manager includes in a profile.

The test was mostly successful, but there are still work that needs to be done to the parsing. For example:

* Some values are missed in parsing as the regexes aren't matching everything they should.
* Payload values with dicts or arrays of dicts are not handled.
* Strings with the prefix **internal_use** reference a value somewhere else in the code that I haven't looked into:  

 ```bash
 key: "internal_use_flag_useCommonAlwaysOnTunnelConfig"
 ```

## Usage

Run this script on a machine which has Server.app located in the Applications folder.

Use the `-l/--list` flag to get a list of all available KnobSets for the current version of Profile Manager:

```console
$ ./profileManagerKeyExtractor.py -l
adCertKnobSets
airplayKnobSets
airprintKnobSets
apnKnobSets
appConfigurationKnobSets
appLockKnobSets
calDavKnobSets
cardDavKnobSets
certificateKnobSets
cfprefsKnobSets
directoryKnobSets
dockKnobSets
energySaverKnobSets
exchangeKnobSets
finderKnobSets
fontsKnobSets
generalKnobSets
globalHttpProxyKnobSets
googleAccountKnobSets
homeScreenLayoutKnobSets
iChatKnobSets
identificationKnobSets
interfaceKnobSets
ldapKnobSets
lockScreenMessageKnobSets
loginItemKnobSets
loginWindowKnobSets
macRestrictionsKnobSets
mailKnobSets
managedDomainsKnobSets
mobilityKnobSets
networkUsageRulesKnobSets
notificationKnobSets
osxserverAccountKnobSets
parentalControlsKnobSets
passcodeKnobSets
printingKnobSets
privacyKnobSets
proxiesKnobSets
restrictionsKnobSets
scepKnobSets
singleSignOnKnobSets
softwareUpdateKnobSets
subscribedCalendarKnobSets
timeMachineKnobSets
universalAccessKnobSets
vpnKnobSets
webClipKnobSets
webContentFilterKnobSets
xsanKnobSets
```

Then, use the `-k/--knobset` flag followed by a KnobSet from the list to print it's payload keys and information.

```console
$ ./profileManagerKeyExtractor.py -k calDavKnobSets

    Payload Name: CalDAV
    Payload Type: com.apple.caldav.account
          Unique: NO
       UserLevel: YES
     SystemLevel: NO
       Platforms: iOS,OSX

      PayloadKey: CalDAVAccountDescription
           Title: Account Description
     Description: The display name of the account
            Type: String
     Hint String: optional
    DefaultValue: My Calendar Account

      PayloadKey: CalDAVHostName
           Title: Account Hostname and Port
     Description: The CalDAV hostname or IP address and port number
            Type: String

      PayloadKey: CalDAVPort
           Title:
     Description:
            Type: Number
    DefaultValue: 8443

      PayloadKey: CalDAVPrincipalURL
           Title: Principal URL
     Description: The Principal URL for the CalDAV account
            Type: String

      PayloadKey: CalDAVUsername
           Title: Account User name
     Description: The CalDAV user name
            Type: String
     Hint String: Required (OTA)
                  Set on device (Manual)

      PayloadKey: CalDAVPassword
           Title: Account Password
     Description: The CalDAV password
            Type: String
     Hint String: Optional (OTA)
                  Set on device (Manual)

      PayloadKey: CalDAVUseSSL
           Title: Use SSL
     Description: Enable Secure Socket Layer communication with CalDAV server
            Type: Boolean
    DefaultValue: YES
```
