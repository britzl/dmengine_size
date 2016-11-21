#!/usr/bin/env python
import urllib
import os
import datetime
import itertools
from csv import reader
import matplotlib
matplotlib.use('Agg')

from matplotlib import pyplot


def get_size(sha1, path):
	url = "http://d.defold.com/archive/" + sha1 + "/" + path
	d = urllib.urlopen(url)
	return d.info()['Content-Length']

engines = [
	{ "platform": "arm64-darwin", "filename": "dmengine_release" },
	{ "platform": "armv7-android", "filename": "dmengine_release.apk" },
	{ "platform": "armv7-darwin", "filename": "dmengine_release" },
	{ "platform": "darwin", "filename": "dmengine_release" },
	{ "platform": "js-web", "filename": "dmengine_release.js" },
	{ "platform": "linux", "filename": "dmengine_release" },
	{ "platform": "win32", "filename": "dmengine_release.exe" },
	{ "platform": "x86_64-darwin", "filename": "dmengine_release" },
	{ "platform": "x86_64-linux", "filename": "dmengine_release" },
]
releases = [
	{ "version": "1.2.38", "sha1": "d0fdb9c5fc1ac46debbbc39e8ac572b6fa7652f7" },
	{ "version": "1.2.39", "sha1": "4c263ff84c19de1f6304e9c2cf756bf572009d38" },
	{ "version": "1.2.40", "sha1": "b8b46b391ee60a5762024931f92d7cf90650b0dc" },
	{ "version": "1.2.41", "sha1": "95d50f8ef9f04617a6498f6412dac3aab960dc6e" },
	{ "version": "1.2.42", "sha1": "b10ae21d0ef877e91fc91c89d39399d6a8a56caf" },
	{ "version": "1.2.43", "sha1": "a10a45eba9544958b7d64d4dbe90cf8e3eabcf0e" },
	{ "version": "1.2.44", "sha1": "30d355de2d97ef54fabaa53938a52963dec8f88c" },
	{ "version": "1.2.45", "sha1": "4a5a22d288d6bc2806a4a79d2162124f94059b9f" },
	{ "version": "1.2.46", "sha1": "af94d38e4bc8fa29f807025f07b25d6c2d38efe0" },
	{ "version": "1.2.47", "sha1": "445d9ce11e76531c6a3823743617b2937aa2bc8a" },
	{ "version": "1.2.48", "sha1": "4886ef433cd87a45ca5a447af8bc568e4409bd52" },
	{ "version": "1.2.49", "sha1": "84a19985eb2912d17bb571d61473c5d6be66c9b1" },
	{ "version": "1.2.50", "sha1": "44be13348c6547916506d18c763ac96665e21f65" },
	{ "version": "1.2.51", "sha1": "9dcd71c92feb7bbc8bcb00e24c29a6f86d76e97a" },
	{ "version": "1.2.52", "sha1": "1b7762c5433a293fb7181eb8347f776f35ea8e09" },
	{ "version": "1.2.53", "sha1": "a1b8f3d533e7f8713fdee217badce2d1acdc71c2" },
	{ "version": "1.2.54", "sha1": "d9baebe87893f1d220660773a3e7ae8932e6f5a9" },
	{ "version": "1.2.55", "sha1": "ed97ba8447a25c71eeed7b690497ae5a3c42f9a7" },
	{ "version": "1.2.56", "sha1": "c263328a62ce78fcc86941c680670e1f20e6ce98" },
	{ "version": "1.2.57", "sha1": "2b680b3ec7af8a84401ad584d8bc47a246f82947" },
	{ "version": "1.2.58", "sha1": "3ffc1a4f07ca69d5d47ff11e510fff4d7993e5b3" },
	{ "version": "1.2.59", "sha1": "c85517d64288d5d9f2d3bad146dd192687a6b493" },
	{ "version": "1.2.60", "sha1": "f0b34f3292b01184a461f928fcee5aceae741e23" },
	{ "version": "1.2.61", "sha1": "bfa38969ef225100fb5d9a1c43414d882f17f09a" },
	{ "version": "1.2.62", "sha1": "36f9c452d9ba2ffb14dfbd91b96b963f17ad1a01" },
	{ "version": "1.2.63", "sha1": "7053e150cb4412f3bc7af11562e27ac292e1e408" },
	{ "version": "1.2.64", "sha1": "1a026deefcdb40e8251606a1c20ec665e277dcd9" },
	{ "version": "1.2.65", "sha1": "39f180d1fc4ee616bd9e29a321bd58845317a939" },
	{ "version": "1.2.66", "sha1": "b8e108961099b9b70ff82476bed03f6d6606ef4f" },
	{ "version": "1.2.67", "sha1": "dd97a77bb97cde6a6a83f2dd25c3884751e9511f" },
	{ "version": "1.2.68", "sha1": "dd13311deab181d63775c04be935656fdcbdd7cf" },
	{ "version": "1.2.69", "sha1": "18ac5ddf4e9737833068d6e9f8a9e0230f281b68" },
	{ "version": "1.2.70", "sha1": "864eba8ab0257ac795c9593334c79f4b3cbbbbb6" },
	{ "version": "1.2.71", "sha1": "00c6dbb2506e5b567adec6e6b591e2684914e419" },
	{ "version": "1.2.72", "sha1": "181f1cd0d18716abc26524eb83444ec3b1c3455e" },
	{ "version": "1.2.73", "sha1": "181bfb10b315d75960210b4b19d13379a154a518" },
	{ "version": "1.2.74", "sha1": "5d0293aa4206f0ad6b15c6c373dd85cc24a96454" },
	{ "version": "1.2.75", "sha1": "0929102a19fd1c3d3b655a6fd4120fcc59d96ec2" },
	{ "version": "1.2.76", "sha1": "85b4c750f5994f7e97460c7395f365c24e2fe215" },
	{ "version": "1.2.77", "sha1": "86c9c6e78e532440b82c8400f328730b0d72448e" },
	{ "version": "1.2.78", "sha1": "6b5b6a73cc16d52f2e935bd03c305b6722b73772" },
	{ "version": "1.2.79", "sha1": "683677d7d655e9c7aa3328ce9c72dd126391447d" },
	{ "version": "1.2.80", "sha1": "c7176baed6df55d32c3286ce27c84e1fe45406c4" },
	{ "version": "1.2.81", "sha1": "e8e0c7d8d49d99fa51b90887e8cc5d31d7fbcf6d" },
	{ "version": "1.2.82", "sha1": "5fb9dca1a7303e505c95c53c18a29d69418cb6d3" },
	{ "version": "1.2.83", "sha1": "1f14af3d6d66b328bdcc4b537e5f109c3f4014b9" },
	{ "version": "1.2.84", "sha1": "5eb478decad6398828e764ed07ba582c9423bd0b" },
	{ "version": "1.2.85", "sha1": "69b592ceb2ff974584085b6877506a6ddc14c157" },
	{ "version": "1.2.86", "sha1": "ae263d1a84869f9f7e8d453f86f4591a76bf0564" },
	{ "version": "1.2.87", "sha1": "ad5e4d8464435e6b8a51645b6590e6014a454c86" },
	{ "version": "1.2.88", "sha1": "0a5b3b315212623e0f09ae240702234aa1808992" },
	{ "version": "1.2.89", "sha1": "5ca3dd134cc960c35ecefe12f6dc81a48f212d40" },
	{ "version": "1.2.90", "sha1": "5d25bd72acaca1a4bd97038168f8369d370b3645" },
	{ "version": "1.2.91", "sha1": "618f38b65e8b867ea81c3ef892bb2b2b8cc959ce" },
	{ "version": "1.2.92", "sha1": "619820e3e9df9f588981e816bf77232a05a59eaf" },
	{ "version": "1.2.93", "sha1": "f2c010d1fcfe5c619bfcea890feb84d46ef5f47a" },
]

def create_report():
	with open("report.csv", 'w') as out:
		#out.write(str(datetime.datetime.now()) + "\n")
		out.write("VERSION,")
		line = ""
		for engine in engines:
			line = line + engine["platform"] + ","
		out.write(line.rstrip(",") + "\n")
		for release in releases:
			line = ""
			print("Getting size for version " + release["version"])
			line = line + release["version"] + ","
			for engine in engines:
				path = "engine/{}/{}".format(engine["platform"], engine["filename"])
				size = get_size(release["sha1"], path)
				line = line + str(size) + ","
			out.write(line.rstrip(",") + "\n")


def create_graph():
	with open('report.csv', 'r') as f:
		data = list(reader(f))

		# get all versions, ignore column headers
		versions = [i[0] for i in data[1::]]
		xaxis_version = range(0, len(versions))

		fig, ax = pyplot.subplots(figsize=(20, 10))
		pyplot.xticks(xaxis_version, versions, rotation=270)
		for engine, marker in zip(range(1,len(data[0])), itertools.cycle('.o8s+xD*p')):
			yaxis_size = [i[engine] for i in data[1::]]
			ax.plot(xaxis_version, yaxis_size, label=data[0][engine], marker=marker)

		locs,labels = pyplot.yticks()
		pyplot.yticks(locs, map(lambda x: "%d" % x, locs))
		pyplot.ylabel('SIZE')
		pyplot.xlabel('VERSION')
		pyplot.annotate(str(datetime.datetime.now()), xy=(0.05, 0.95), xycoords='axes fraction')

		legend = ax.legend(loc='center right', bbox_to_anchor=(1.4, 0.5))
		frame = legend.get_frame()
		frame.set_facecolor('0.90')

		fig.savefig('size.png', format='png', bbox_extra_artists=(legend,), bbox_inches='tight')

create_report()
create_graph()
