#!/usr/bin/env python

import argparse
import os.path
import mmap
import re
import sys

'''/////////////////'''
'''//  VARIABLES  //'''
'''/////////////////'''

# Payload List
payloads=[]

# Paths
file_pm_javascript_packed = "/Applications/Server.app/Contents/ServerRoot/usr/share/devicemgr/frontend/admin/common/app/javascript-packed.js"
filr_pm_localized_strings = "/Applications/Server.app/Contents/ServerRoot/usr/share/devicemgr/frontend/admin/en.lproj/app/javascript_localizedStrings.js"
folder_backend_models = "/Applications/Server.app/Contents/ServerRoot/usr/share/devicemgr/backend/app/models"



'''/////////////////'''
'''//   CLASSES   //'''
'''/////////////////'''

class sgr_color:
    clr = '\033[0m'
    bld = '\033[1m'

class payload(object):

	# Title
	@property
	def title(self):
		return self._title
	@title.setter
	def title(self, value):
		self._title = expandLocalizedString(cleanString(value))

	# Description
	@property
	def description(self):
		return self._description
	@description.setter
	def description(self, value):
		self._description = expandLocalizedString(cleanString(value))

	# Key
	@property
	def key(self):
		return self._key
	@key.setter
	def key(self, value):
		self._key = value

	# Value Type
	@property
	def type(self):
		return self._type
	@type.setter
	def type(self, value):
		self._type = value

	# Hint String
	@property
	def hint_string(self):
		return self._hint_string
	@hint_string.setter
	def hint_string(self, value):
		isAutoPushMatch = re.search(r'\"isAutoPush\"\)(\?.*?)(;|$)', value, re.DOTALL)
		if isAutoPushMatch:
			hint_string_list = []
			isAutoPush = re.search('\?(.*?):', isAutoPushMatch.group(1), re.DOTALL)
			isNotAutoPush = re.search('\:(.*?);?$', isAutoPushMatch.group(1), re.DOTALL)
			if isAutoPush:
				hint_string_list.append(expandLocalizedString(cleanString(isAutoPush.group(1))) + ' (OTA)')
			if isNotAutoPush:
				hint_string_list.append(expandLocalizedString(cleanString(isNotAutoPush.group(1))) + ' (Manual)')
			if hint_string_list:
				self._hint_string = hint_string_list
		else:
			self._hint_string = expandLocalizedString(cleanString(value))

	# Required
	@property
	def required(self):
		return self._required
	@required.setter
	def required(self, value):
		self._required = value

	# Optional
	@property
	def optional(self):
		return self._optional
	@optional.setter
	def optional(self, value):
		self._optional = value

	# Default Value
	@property
	def default_value(self):
		return self._default_value
	@default_value.setter
	def default_value(self, value):
		self._default_value = expandLocalizedString(cleanString(value))

	# Available Values
	@property
	def available_values(self):
		return self._available_values
	@available_values.setter
	def available_values(self, value):
		self._available_values = value

class knobSet(object):

	# PayloadType
	@property
	def payload_type(self):
		return self._payload_type
	@payload_type.setter
	def payload_type(self, value):
		self._payload_type = value

	# PayloadName
	@property
	def payload_name(self):
		return self._payload_name
	@payload_name.setter
	def payload_name(self, value):
		self._payload_name = value

	# Payloads
	@property
	def payloads(self):
		return self._payloads
	@payloads.setter
	def payloads(self, value):
		self._payloads = value

	# Platforms
	@property
	def platforms(self):
		return self._platforms
	@platforms.setter
	def platforms(self, value):
		self._platforms = value
	
	# SystemLevel
	@property
	def system_level(self):
		return self._system_level
	@system_level.setter
	def system_level(self, value):
		self._system_level = value.replace('\n', '')

	# UserLevel
	@property
	def user_level(self):
		return self._user_level
	@user_level.setter
	def user_level(self, value):
		self._user_level = value.replace('\n', '')

	# Unique
	@property
	def unique(self):
		return self._unique
	@unique.setter
	def unique(self, value):
		if value == 'false':
			self._unique = 'NO'
		elif value == 'true':
			self._unique = 'YES'
		else:
			print 'UNKNOWN UNIQUE: ' + value

'''/////////////////'''
'''//   METHODS   //'''
'''/////////////////'''

lowercase = lambda s: s[:1].lower() + s[1:] if s else ''

def cleanString(string):
	if string:
		return re.sub(r'\.loc\(\)', '', string).replace('\n', '')

def expandLocalizedString(string):
	quoteMatch = '["\']'
	if string.startswith('"'):
		aString = string.replace("\'", "\\'")
		quoteMatch = '"'
	elif string.startswith("'"):
		aString = string.replace('"', '\"')
		quoteMatch = '\''
	else:
		aString = string

	bString = re.sub(r'(^"|"$)', '', aString)
	cString = bString.replace('(', '\(')
	cleanedString = cString.replace(')', '\)')

	with open(filr_pm_localized_strings, 'r') as f:
		file_content = mmap.mmap(f.fileno(), 0, prot=mmap.PROT_READ)
		locString = re.search('["\']' + cleanedString + '["\']' + ': ["\'](.*?)["\'],', file_content, re.DOTALL)
		if locString:
			return locString.group(1)
	return string

def knobSetList(file_path):
	with open(file_path, 'r') as f:
		file_content = mmap.mmap(f.fileno(), 0, prot=mmap.PROT_READ)
		knobSetListMatch = re.search('knobSetProperties:\[([",a-zA-Z]+)\],', file_content)
		if knobSetListMatch:
			return knobSetListMatch.group(1).translate(None, ' "').split(',')

def parseChildViews(knobSetPayload, knobSetExtendMatch, knobSetRealName, child_views, string):

	# Create an empty variable for the view last processed, used later to prevent infinite looping.
	last_views = []

	# Loop through all view names from list child_views
	for view in child_views:
		#print 'View: ' + view

		# Get Title
		viewContentLabel = re.search(knobSetRealName + 'Label:.*?\({(.*?)\)},.*?:(Admin|SC)', string, re.DOTALL)
		if viewContentLabel:
			title = re.search('value:(["\'].*?)[,}]', viewContentLabel.group(1), re.DOTALL)
			if title:
				knobSetPayload.title = title.group(1)

		# Get Description
		viewContentDescription = re.search(knobSetRealName + 'Description:.*?\({(.*?)},.*?:(Admin|SC)', string, re.DOTALL)
		if viewContentDescription:
			description = re.search('value:(["\'].*?)[,}]', viewContentDescription.group(1), re.DOTALL)
			if description:
				knobSetPayload.description = description.group(1)

		# Get Available Values
		if view == knobSetRealName + 'SelectView':
			viewContentSelection = re.search(knobSetRealName + 'SelectView:.*?\({(.*?},.*?):(Admin|SC)', string, re.DOTALL)
			if viewContentSelection:
				viewContentSelectionObjects = re.search('objects:\[(.*?)\],', viewContentSelection.group(1), re.DOTALL)
				if viewContentSelectionObjects:
					available_values = re.findall(r'\{.+?\}', viewContentSelectionObjects.group(1).replace('\n', ''))
					if available_values:
						knobSetPayload.available_values = available_values

		# Get the contents of the view's method, try three different regexes to match multiple scenarios.
		viewContent = re.search(view + ':.*?\({(.*?}\)?,[a-zA-Z]+):(Admin|SC)', string, re.DOTALL)
		if not viewContent:
			# Matches last method
			viewContent = re.search(view + ':.*?\({(.*?)}\)}\)', string, re.DOTALL)
			if not viewContent:
				# Matches any method "starting" with view name
				viewContent = re.search(view + '[a-zA-Z]+:.*?\({(.*?}\)?,[a-zA-Z]+):(Admin|SC)', string, re.DOTALL)

		if viewContent:

			# Check if method body contains variable (field)[Cc]ontentValueKey
			contentValueKey = re.search('[Cc]ontentValueKey:"(.*?)"', viewContent.group(1), re.DOTALL)
			if contentValueKey:

				# Check if contentValueKey matches current knob set name.
				# If it matches, get title, and description info from this body.
				if (( contentValueKey.group(1).lower() == knobSetRealName.lower() ) or ( contentValueKey.group(1).lower() == re.sub(r'^_', '', knobSetRealName.lower())) or  ( contentValueKey.group(1).lower() == 'name' )):
					label = re.search('label:(["\'].*?)(?:,[a-zA-Z]+|})', viewContent.group(1), re.DOTALL)
					if label:
						knobSetPayload.title = label.group(1)

					title = re.search('title:(["\'].*?)(?:,[a-zA-Z]+|})', viewContent.group(1), re.DOTALL)
					if title:
						knobSetPayload.title = title.group(1)

					#description = re.search('description:(["\'].*?)[,}]', viewContent.group(1), re.DOTALL)
					description = re.search('description:(["\'].*?)(?:,[a-zA-Z]+|})', viewContent.group(1), re.DOTALL)
					if description:
						knobSetPayload.description = description.group(1)

					fieldObjects = re.search('(?:(?:field)?[Oo]bjects|items):\[(.*?)\],', viewContent.group(1), re.DOTALL)
					if fieldObjects:
						available_values = re.findall(r'\{.+?\}', fieldObjects.group(1).replace('\n', ''))
						if available_values:
							knobSetPayload.available_values = available_values

					hint = re.search('[Hh]int:(.*?)[,}]', viewContent.group(1), re.DOTALL)
					if hint:
						knobSetPayload.hint_string = hint.group(1)
					break

				# If contentValueKey didn't match current knob set name, get all funcion names in knobSetExtendMatch. 
				'''#if view.startswith(knobSetRealName) or view.startswith(re.sub(r'^_', '', knobSetRealName)):'''
				
				# This can be removed.
				functionContentMatch = re.findall('[,}]([_a-zA-Z]+:function.*?\.property\(\".*?\")', knobSetExtendMatch[0].replace('\n', ''), re.DOTALL)
				if functionContentMatch:

					# Check if contentValueKey matches the property value of any function in knobSetExtendMatch
					# Check if that property value matches current knob set name.
					# If it matches, get title, and description info from this body.
					functionContent = re.search(contentValueKey.group(1) + ':function.*?\.property\(\"(.*?)\"', knobSetExtendMatch[0].replace('\n', ''), re.DOTALL)
					if functionContent and functionContent.group(1).lower() == knobSetRealName.lower():
						label = re.search('label:(["\'].*?)(?:,[a-zA-Z]+|})', viewContent.group(1), re.DOTALL)
						if label:
							knobSetPayload.title = label.group(1)

						title = re.search('title:(["\'].*?)(?:,[a-zA-Z]+|})', viewContent.group(1), re.DOTALL)
						if title:
							knobSetPayload.title = title.group(1)

						#description = re.search('description:(["\'].*?)[,}]', viewContent.group(1), re.DOTALL)
						description = re.search('description:(["\'].*?)(?:,[a-zA-Z]+|})', viewContent.group(1), re.DOTALL)
						if description:
							knobSetPayload.description = description.group(1)

						fieldObjects = re.search('(?:(?:field)?[Oo]bjects|items):\[(.*?)\],', viewContent.group(1), re.DOTALL)
						if fieldObjects:
							available_values = re.findall(r'\{.+?\}', fieldObjects.group(1).replace('\n', ''))
							if available_values:
								knobSetPayload.available_values = available_values

						hint = re.search('[Hh]int:(.*?)[,}]', viewContent.group(1), re.DOTALL)
						if hint:
							knobSetPayload.hint_string = hint.group(1)
						break

			# If string doesn't contain 'fieldContentValueKey' it might contain additinal subviews. 
			# Loop through those as well.
			knobSetSubViews = re.search('childViews:\[(.*?)\],', viewContent.group(1), re.DOTALL)
			if knobSetSubViews and not set(knobSetSubViews.group(1).translate(None, ' "').split(',')).intersection(last_views):
				last_views = knobSetSubViews.group(1).translate(None, ' "').split(',')
				parseChildViews(knobSetPayload, knobSetExtendMatch, knobSetRealName, last_views, string)
		else:
			print 'NO VIEW CONTENT IN: ' + view


def knobSetInfo(file_path, knobSetPropertyName):

	# Instantiate a new knobSet class instance
	newKnobSet = knobSet()

	# Open javascript-packed.js for parsing
	with open(file_path, 'r') as f:
		file_content = mmap.mmap(f.fileno(), 0, prot=mmap.PROT_READ)

		# Get KnobSet 'Name' used in functions
		knobSetNameMatch = re.search(',Admin.([a-zA-Z]+?KnobSet).*?profilePropertyName[=:]"' + knobSetPropertyName, file_content)
		if not knobSetNameMatch:
			print 'Could not find KnobSet Name for: ' + knobSetPropertyName
			sys.exit()
		else:
			knobSetName = knobSetNameMatch.group(1)
			print knobSetName

		# Get KnobSet 'DisplayName' string to extract the file name for the ruby model
		knobSetNumLinesMatch = re.search(',Admin.' + knobSetName + '.*?numLines[=:]"(.*?)"', file_content)
		if not knobSetNumLinesMatch:
			print 'Could not find KnobSet DisplayName for: ' + knobSetPropertyName
			sys.exit()
		else:
			knobSetDisplayName = re.sub(r'(^_global_?|^_|_num_lines$)', '', knobSetNumLinesMatch.group(1))

		# Get path to ruby model and verify it exists.
		modelPath = folder_backend_models + '/' + knobSetDisplayName + '.rb'
		if not os.path.isfile(modelPath):
			print 'File doesn\'t exist: ' + modelPath

		# Open ruby model file for parsing
		with open(modelPath, 'r') as fmodel:
			model_file_content = mmap.mmap(fmodel.fileno(), 0, prot=mmap.PROT_READ)

			# Get PayloadType (or Types if the KnobSet allows multiple)
			payloadType = re.search(r'@@payload_type[ ]+=[ ]+?[\'"]?(.*?)[\'"]?[\n]', model_file_content, re.DOTALL)
			if payloadType:
				newKnobSet.payload_type = payloadType.group(1)
			else:
				payloadTypes = re.search(r'@@payload_types[ ]+=[ ]+?{(.*?)}', model_file_content, re.DOTALL)
				if payloadTypes:
					payloadTypeStringList = []
					for payloadTypeListItem in payloadTypes.group(1).translate(None, ' \n').split(','):
						if not payloadTypeListItem:
							continue
						payloadTypeGroup = re.search(r'^(.*?)\=\>(.*?)$', payloadTypeListItem, re.DOTALL)
						if payloadTypeGroup:
							payloadTypeStringList.append(payloadTypeGroup.group(1) + ': ' + payloadTypeGroup.group(2))
							newKnobSet.payload_type = payloadTypeStringList

			# Get boolean wether this payload is unique or supports multiple payloads
			isUnique = re.search(r'@@is_unique[ ]+=[ ]+?[\'"]?(.*?)[\'"]?[\n]', model_file_content, re.DOTALL)
			if isUnique:
				newKnobSet.unique= isUnique.group(1)

			# Get the name for the KnobSet, shown as the title for the payload group
			payloadName = re.search(r'@@payload_name[ ]+=[ ]+?[\'"]?(.*?)[\'"]?[\n]', model_file_content, re.DOTALL)
			if payloadName:
				newKnobSet.payload_name = payloadName.group(1)

		# Get SCMixin Info for 'knobSetName'
		knobSetSCMixinMatch = re.findall('SC.mixin\(Admin.' + knobSetName + ',{(.*?)}\),Admin.' , file_content, re.DOTALL)
		if not knobSetSCMixinMatch:
			knobSetSCMixinMatch = re.findall('Admin.' + knobSetName + '.mixin\({(.*?)}\),Admin.' , file_content, re.DOTALL)
			if not knobSetSCMixinMatch:
				print 'Could not find mixin for: ' + knobSetSCMixinMatch
				sys.exit()

		# Get what platforms payload supports
		platformTypes = re.search('platformTypes:"(.*?)"', knobSetSCMixinMatch[0], re.DOTALL)
		if platformTypes:
			newKnobSet.platforms = platformTypes.group(1).split()

		# Get if payload is available as 'System Level'
		systemLevel = re.search('systemLevel:"(.*?)"', knobSetSCMixinMatch[0], re.DOTALL)
		if not systemLevel:
			systemLevel = re.findall('Admin.' + knobSetName + '.systemLevel=(.*?),Admin.' , file_content, re.DOTALL)
			if not systemLevel:
				# FIXME - THIS IS NOT RIGHT
				systemLevel = re.findall('Admin.' + knobSetName + '.*?systemLevel[=:](.*?),.*?}\),Admin.' , file_content, re.DOTALL)
			if systemLevel:
				newKnobSet.system_level = systemLevel[0]
		else:
			newKnobSet.system_level = systemLevel.group(1).split()

		# Get if payload is available as 'User Level'
		userLevel = re.search('userLevel:"(.*?)"', knobSetSCMixinMatch[0], re.DOTALL)
		if not userLevel:
			userLevel = re.findall('Admin.' + knobSetName + '.userLevel=(.*?),Admin.' , file_content, re.DOTALL)
			if not userLevel:
				# FIXME - THIS IS NOT RIGHT
				userLevel = re.findall('Admin.' + knobSetName + '.*?userLevel[=:](.*?)}\),Admin.' , file_content, re.DOTALL)
			if userLevel:
				newKnobSet.user_level = userLevel[0]
		else:
			newKnobSet.user_level = userLevel.group(1).split()

		# Get KnobSetExtendView Info for 'knobSetName'
		knobSetViewExtendMatch = re.findall(',Admin.' + knobSetName + 'View=Admin.KnobSetView.extend\({(.*?)}\),Admin.' , file_content, re.DOTALL)		
		if not knobSetViewExtendMatch:
			print 'Could not find KnobSetExtendView for: ' + knobSetName
			sys.exit()

		# Get all child view names from KnobSetExtendedView
		knobSetViewsMatch = re.findall('childViews:\[(.*?)\],', knobSetViewExtendMatch[0].replace('\n', ''), re.DOTALL)
		if knobSetViewsMatch:
			knobSetViews = (",".join(knobSetViewsMatch)).translate(None, ' "').split(',')

		# Get KnobSetExtend Info for 'knobSetName'
		knobSetExtendMatch = re.findall(',Admin.' + knobSetName + '=Admin.KnobSet.extend\({(.*?)}\),Admin.' , file_content, re.DOTALL)
		if not knobSetNameMatch:
			print 'Could not find KnobSetExtend for' + knobSet
			sys.exit()
	
		knobSetPayloads = []
		knobSetProperties = re.findall(',?([_a-zA-Z]+:SC.Record.attr\(.*?)}\)', knobSetExtendMatch[0].replace('\n', ''), re.DOTALL)
		for knobSetProperty in knobSetProperties:

			# Instantiate new payload class
			knobSetPayload = payload()

			# Get the knobSetProperty: name
			knobSetRealNameMatch = re.search(r'^(.*?):', knobSetProperty, re.DOTALL)
			if not knobSetRealNameMatch:
				print 'Could not find KnobSetRealName for' + knobSet
				sys.exit()
			elif knobSetRealNameMatch.group(1).startswith('real'):
				knobSetRealName = lowercase(re.sub(r'^real', '', knobSetRealNameMatch.group(1)))
			else:
				knobSetRealName = knobSetRealNameMatch.group(1)

			# Get the knobSetProperty: title, description
			parseChildViews(knobSetPayload, knobSetExtendMatch, knobSetRealName, knobSetViews, knobSetViewExtendMatch[0].replace('\n', ''))

			# Get Payload Key
			propertyKeyMatch = re.search('key:"(.*?)"', knobSetProperty, re.DOTALL)
			if propertyKeyMatch:
				knobSetPayload.key = propertyKeyMatch.group(1).replace('\n', '')

			# Get Payload Value Type
			propertyTypeMatch = re.search('SC.Record.attr\((.*?),', knobSetProperty, re.DOTALL)
			if propertyTypeMatch:
				knobSetPayload.type = propertyTypeMatch.group(1).replace('\n', '')

			# Get Payload Required
			propertyRequiredMatch = re.search('isRequired:(YES|NO)', knobSetProperty, re.DOTALL)
			if propertyRequiredMatch:
				knobSetPayload.required = propertyRequiredMatch.group(1).replace('\n', '')

			# Get Payload Default Value
			try:
				#print 'knobSetProperty: ' + knobSetProperty
				if knobSetPayload.type == 'Array' :
					regex_string = 'defaultValue:.*\[(.*?)\]'
				else:
					regex_string = 'defaultValue:(.*)[,}]?'
			except AttributeError:
				regex_string = 'defaultValue:(.*)[,}]?'

			propertyDefaultValueMatch = re.search(r'%s' % regex_string, knobSetProperty, re.DOTALL)
			if propertyDefaultValueMatch:
				try:
					if knobSetPayload.type == 'Array':
						knobSetPayload.default_value = re.findall(r'\{.+?\}', propertyDefaultValueMatch.group(1).replace('\n', ''))
					else:
						knobSetPayload.default_value = propertyDefaultValueMatch.group(1).replace('\n', '')
				except AttributeError:
					knobSetPayload.default_value = propertyDefaultValueMatch.group(1).replace('\n', '')

			# Add payload to array
			knobSetPayloads.append(knobSetPayload)

		# Return all payloads found
		newKnobSet.payloads = knobSetPayloads
		return newKnobSet

def printKnobSet(file_path, knobSetPropertyName):

	# Populate a new knobset class instance for selected knobSet
	newKnobSet = knobSetInfo(file_path, knobSetPropertyName)

	# Add newline
	print ''

	try:
		print '%18s' % 'Payload Name: ' + newKnobSet.payload_name
	except AttributeError:
		print '%17s' % 'Payload Name:'

	try:
		if isinstance(newKnobSet.payload_type, list):
			firstValue = True
			for payloadType in newKnobSet.payload_type:
				if firstValue:
					firstValue = False
					print '%18s' % 'Payload Types: ' + payloadType
				else:
					print '%18s' % '' + payloadType
		else:
			print '%18s' % 'Payload Type: ' + newKnobSet.payload_type
	except AttributeError:
		print '%17s' % 'Payload Type:'

	try:
		print '%18s' % 'Unique: ' + newKnobSet.unique
	except AttributeError:
		print '%17s' % 'Unique:'

	# Using the values in the knobSet class, print to stdout:
	# User Level
	try:
		print '%18s' % 'UserLevel: ' + newKnobSet.user_level
	except AttributeError:
		print '%17s' % 'UserLevel:'

	# System Level
	try:
		print '%18s' % 'SystemLevel: ' + newKnobSet.system_level
	except AttributeError:
		print '%17s' % 'SystemLevel:'

	# Platforms
	try:
		sys.stdout.write('%18s' % 'Platforms: ')
		print(','.join(newKnobSet.platforms))
	except AttributeError:
		pass

	# PayloadKey Info
	for p in newKnobSet.payloads:
		print '\n%18s' % 'PayloadKey: ' + sgr_color.bld + p.key + sgr_color.clr
		
		try:
			print '%18s' % 'Title: ' + expandLocalizedString(p.title)
		except AttributeError:
			print '%17s' % 'Title:'

		try:
			print '%18s' % 'Description: ' + p.description
		except AttributeError:
			print '%17s' % 'Description:'

		print '%18s' % 'Type: ' + p.type

		try:
			print '%18s' % 'Required: ' + p.required
		except AttributeError:
			pass

		try:
			print '%18s' % 'Optional: ' + p.optional
		except AttributeError:
			pass

		try:
			if p.hint_string and isinstance(p.hint_string, list):
				firstValue = True
				for hint_string in p.hint_string:
					if firstValue:
						firstValue = False
						print '%18s' % 'AvailableValues: ' + hint_string
					else:
						print '%18s' % '' + hint_string
			elif p.default_value:
				print '%18s' % 'Hint String: ' + p.hint_string
		except AttributeError:
			pass

		try:
			firstValue = True
			for available_value in p.available_values:
				value = re.search('value:(["\']?.*?)[,}]', available_value, re.DOTALL)
				if value:
					if firstValue:
						firstValue = False
						print '%18s' % 'AvailableValues: ' + value.group(1)
					else:
						print '%18s' % '' + value.group(1)
		except AttributeError:
			pass

		try:
			if p.default_value and isinstance(p.default_value, list):
				sys.stdout.write('%18s' % 'DefaultValue: ')
				print("\t\n\t\t\t".join(p.default_value))
			elif p.default_value:
				print '%18s' % 'DefaultValue: ' + p.default_value
		except AttributeError:
			pass
	sys.exit()

def main(argv):

	# Parse input arguments
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--file', type=str)
	parser.add_argument('-l', '--list', action='store_true')
	parser.add_argument('-k', '--knobset', type=str)
	args = parser.parse_args()

	# Get path to javascript file.
	if args.file:
		file_path = args.file
	else:
		file_path = file_pm_javascript_packed

	# Verify passed file path is valid
	if not os.path.isfile(file_path):
		print 'file doesn\'t exist: ' + file_path
		sys.exit()

	# Create array of all available KnobSet names from the 'knobSetProperties' array.
	knobSets = knobSetList(file_path)
	if not knobSets:
		print 'Found no KnobSet array in passed file, are you sure Server.app is installed and the file path is correct?'
		sys.exit()

	# If option -l/--list was passed, list all KnobSets available
	if args.list:
		print("\n".join(sorted(knobSets)))
		sys.exit()

	# If option -k/--knobset was passed, print info for passed KnobSet
	if args.knobset:
		if not args.knobset in knobSets:
			print args.knobset + ' is not a valid KnobSet.'
			print 'To see all available KnobSets, use the -l flag'
			sys.exit()
		printKnobSet(file_path, args.knobset)

	print 'No option was passed.'
	print 'To see all available KnobSets, use the -l flag'

if __name__ == "__main__":
    main(sys.argv[1:])