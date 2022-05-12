import requests
import sys
import re
import optparse
from optparse import OptionParser

if (len(sys.argv) != 5 and '-h' not in sys.argv):
	print("Usage: \033[33mpython3 %s -s [base_gitlab_url] -t [personal_access_token]\033[0m" % sys.argv[0])
	print("Example: \033[33mpython3 %s -s https://api.gitlab.com -t reallycooltoken\033[0m" % sys.argv[0])
	sys.exit(0)

parser = OptionParser()
parser.add_option("-t", "--token", help="Gitlab personal access token")
parser.add_option("-s", "--server", help="Gitlab server base url (ex: https://api.gitlab.com)")
(options,args) = parser.parse_args()
idlist = []
grouplist = []
projlist = []
pipelinelist = []
names = []

token = options.token
server = options.server
uagent = 'Mozilla/5.0 (MacIntosh; Intel Mac OS X 10_15_7) appleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
headers = {'User-Agent': uagent, 'PRIVATE-TOKEN': token}

def ListProjects(headers):
	print("\033[92m======================Attempting To List Projects=======================\033[0m")
	projurl = server + '/api/v4/projects'
	response = requests.get(projurl,headers=headers).json()

	for p in response:
		try:
			idval = p['id']
			projlist.append(idval)
			idlist.append(idval)
			desc = p['description']
			pwn = p['path_with_namespace']
			ca = p['created_at']
			db = p['default_branch']
			la = p['last_activity_at']
			#print("id: %s\ndescription: %s\npath: %s\ncreated: %s\nlast activity: %s"%(idval,desc,pwn,ca,la))
			print("id: %s\ndescription: %s\npath: %s\ncreated: %s\ndefault branch: %s\nlast activity: %s"%(idval,desc,pwn,ca,db,la))
			print("\033[33m===========================================================\033[0m")
		except:
			pass


def ListJobs(headers):
	print("\033[92m======================Attempting To List Jobs=======================\033[0m")
	for each in idlist:
		response = requests.get(server + '/api/v4/projects/%s/jobs'%each,headers=headers).json()
		for p in response:
			try:
				jid = p['id']
				status = p['status']
				stage = p['stage']
				nm = p['name']
				ref = p['ref']
				cid = p['commit']['id']
				author = p['commit']['author_email']
				aname = p['commit']['author_name']
				created = p['commit']['created_at']
				msg = p['commit']['message']
				title = p['commit']['title']
				duration = p['duration']
				artifacts = p['artifacts']
				wurl = p['web_url']
				uid = p['user']['id']
				uname = p['user']['name']
				usrname = p['user']['username']
				print("job id: %s\nStatus: %s\nStage: %s\nName: %s\nRef: %s\nCommit ID: %s\nCommitter Email: %s\nCommitter Author: %s\nCommit Created At: %s\nCommit Msg: %s\nCommit Title: %s\nCommit Duration: %s\nArtifacts: %s\nWeb url: %s\nUser ID: %s\nUser Name: %s\nusername: %s"%(jid,status,stage,nm,ref,cid,author,aname,created,msg,title,duration,artifacts,wurl,uid,uname,usrname))
				print("\033[33m===========================================================\033[0m")
			except:
				pass



def ListBranches(headers):
	print("\033[92m======================Attempting To List Branch Info=======================\033[0m")

	for each in idlist:
		response = requests.get(server + '/api/v4/projects/%s/repository/branches'%each,headers=headers).json()
		for p in response:
			try:
				nameval = p['name']
				permission = p['can_push']
				cid = p['commit']['id']
				cdate = p['commit']['created_at']
				msg = p['commit']['message']
				author = p['commit']['author_name']
				cmt_email = p['commit']['committer_email']
				protected = p['protected']
				canpush = p['developers_can_push']
				canmerge = p['developers_can_merge']
				url = p['web_url']
				print("Branch Name: %s\nCan_Push_To_Branch: %s\nCommit ID: %s\nCommit Created At: %s\nCommit_Message: %s\nCommit_Author: %s\nCommiter_Email: %s\nProtected: %s\nDevelopers_Can_Push: %s\nDevelopers_Can_Merge: %s\nurl: %s"%(nameval,permission,cid,cdate,msg,author,cmt_email,protected,canpush,canmerge,url))
				print("\033[33m===========================================================\033[0m")
			except:
				pass

def ListGroups(headers):
	print("\033[92m======================Attempting To List Group Info For This User=======================\033[0m")
	response = requests.get(server + '/api/v4/groups',headers=headers).json()
	for p in response:
		try:
			idval = p['id']
			grouplist.append(idval)
			name = p['full_name']
			path = p['path']
			desc = p['description']
			visibility = p['visibility']
			pcl = p['project_creation_level']
			scl = p['subgroup_creation_level']
			weburl = p['web_url']
			print("Group id: %s\nGroup Name: %s\nGroup Path: %s\nGroup Description: %s\nGroup Visibility: %s\nProject_Creation_Level: %s\nSubGroup Creation Level: %s\nWeb_url: %s"%(idval,name,path,desc,visibility,pcl,scl,weburl))
			print("\033[33m===========================================================\033[0m")
		except:
			pass

def ListProjectPipelinesVariables(headers):
	print("\033[92m======================Attempting To List Project Pipeline Variables (may contain creds)=======================\033[0m")
	c = 0
	for each in projlist:
		if isinstance(each,int):
			response = requests.get(server + '/api/v4/projects/%s/pipelines'%each,headers=headers).json()
		for p in response:
			try:
				id = p['id']
				pipelinelist.append(id)
			except:
				pass
		pipelineset = set(pipelinelist)
		pipelinelist2 = list(pipelineset)

		for x in pipelinelist2:
			response2 = requests.get(server + '/api/v4/projects/%s/pipelines/%s/variables'%(each,x),headers=headers).json()
			for each in response2:
				if each != "message":
					c = c + 1
	if c == 0:
		print("[-] No Project Pipeline Variables found")
		print("\033[33m===========================================================\033[0m")
	else:
		for each in response2:
			print(each)
			print("\033[33m===========================================================\033[0m")


def ListProjectVariables(headers):
	print("\033[92m======================Attempting To List Project Variables (may contain creds)=======================\033[0m")
	c = 0
	for each in projlist:
		if isinstance(each,int):
			response = requests.get(server + '/api/v4/projects/%s/variables'%each,headers=headers).json()
		for p in response:
			if p != "message":
				c = c + 1

	if c == 0:
		print("[-] No Project Variables found")
		print("\033[33m===========================================================\033[0m")
	else:
		for each in response:
			print(each)
			print("\033[33m===========================================================\033[0m")


def PersonalAccessTokens(headers):
	print("\033[92m======================Attempting To Display Info On Personal Access Tokens For This User=======================\033[0m")
	response = requests.get(server + '/api/v4/personal_access_tokens',headers=headers).json()
	for p in response:
		try:
			id = p['id']
			name = p['name']
			revoked = p['revoked']
			created = p['created_at']
			scopes = p['scopes']
			active = p['active']
			userid = p['user_id']
			expires = p['expires_at']
			print("PAT id: %s\nPAT Name: %s\nRevoked: %s\nCreated At: %s\nScopes: %s\nActive: %s\nUser_id: %s\nExpires At: %s"%(id,name,revoked,created,scopes,active,userid,expires))
			print("\033[33m===========================================================\033[0m")
		except:
			pass


ListProjects(headers)
ListBranches(headers)
ListJobs(headers)
ListGroups(headers)
PersonalAccessTokens(headers)
ListProjectVariables(headers)
ListProjectPipelinesVariables(headers)
