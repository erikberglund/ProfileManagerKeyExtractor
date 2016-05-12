## ProfileManagerKeyExtractor

Script to extract payload information from the Profile Manager source code.

**NOTE: This script is not finished as it currently doesn't handle all payload keys and value types**

Here's a link to my companion blog post about this script: [Extracting Payload Keys From Profile Manager]() 

I've written this script to test the possibility of extracting payload information directly from a Profile Manager installation to circumvent having to create and export profiles from the GUI in order to find the keys Profile Manager includes in a profile.

The test was mostly successful, but there are still work that needs to be done to the parsing on the more complex structures, like payloads which take a single or nested dicts, or an array of dicts for example.

There are also some strings returned with prefix **internal_use** that reference a value somewhere else in the code that I haven't looked into yet:

_Example:_

```bash
key: "internal_use_flag_useCommonAlwaysOnTunnelConfig"
```

## Usage

Run this script on a manchine which has Server.app located in the Applications folder.

Use the `-l/--list` flag to get a list of all available KnobSets for the current version of Profile Manager:

```bash
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

Then, use the `-k/--knobset` flag followed by a KnobSet from the list to print it's payload key and information.

```bash
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
    DefaultValue: My CalDAV Account

      PayloadKey: CalDAVHostName
           Title: Account Hostname and Port
     Description: The CalDAV hostname or IP address and port number
            Type: String
     Hint String: required

      PayloadKey: CalDAVPort
           Title:
     Description:
            Type: Number
    DefaultValue: 8443

      PayloadKey: CalDAVPrincipalURL
           Title: Principal URL
     Description: The Principal URL for the CalDAV account
            Type: String
     Hint String: optional

      PayloadKey: CalDAVUsername
           Title: Account User name
     Description: The CalDAV user name
            Type: String
     Hint String: (OTA: required)
                  (Manual: set on device)

      PayloadKey: CalDAVPassword
           Title: Account Password
     Description: The CalDAV password
            Type: String
     Hint String: (OTA: optional)
                  (Manual: set on device)

      PayloadKey: CalDAVUseSSL
           Title: Use SSL
     Description: Enable Secure Socket Layer communication with CalDAV server
            Type: Boolean
    DefaultValue: YES
```
