## ProfileManagerKeyExtractor

Script to extract payload information from the Profile Manager source code.

**Note: This script is currently just a proof of concept and NOT a finished tool.**

Here's a link to my companion blog post for this script: [Extracting Payload Keys From Profile Manager]() 

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
 AvailableValues: required (OTA)
                  set on device (Manual)

      PayloadKey: CalDAVPassword
           Title: Account Password
     Description: The CalDAV password
            Type: String
 AvailableValues: optional (OTA)
                  set on device (Manual)

      PayloadKey: CalDAVUseSSL
           Title: Use SSL
     Description: Enable Secure Socket Layer communication with CalDAV server
            Type: Boolean
    DefaultValue: YES
```
