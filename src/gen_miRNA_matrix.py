import pandas as pd 
import hashlib
import os,pdb
from utils import logger
import json
def file_as_bytes(file):
    with file:
        return file.read()

def extractMatrix(dirname, start, chunksize):
	count = 0
	RNA_data = []
	num_of_files = 0;
	for idname in os.listdir(dirname):
		if idname.find("-") != -1:
			idpath = dirname +"/" + idname
			if(num_of_files < start*chunksize):
				num_of_files += 1
				continue
			for filename in os.listdir(idpath):
				if filename.find("-") != -1:
					filepath = idpath + "/" + filename
					df = pd.read_csv(filepath,header=None,sep="\t")
					if count ==0:
						RNA_ids = df[0].values[:-5].tolist()
					id_RNA_read_counts = [idname] + df[1].values[:-5].tolist()
					RNA_data.append(id_RNA_read_counts)
					num_of_files += 1
					count +=1
		if num_of_files == ((start+1)*chunksize):
			break
	columns = ["file_id"] + RNA_ids
	df = pd.DataFrame(RNA_data, columns=columns)
	return df

def extractLabel(inputfile):
	df = pd.read_csv(inputfile, sep="\t")
	data = pd.DataFrame(df['cases.0.project.primary_site']+' '+df['cases.0.samples.0.sample_type'],columns=['label'])
	data['file_id'] = df['file_id']
	df.loc[df['cases.0.samples.0.sample_type'].str.contains("Normal"), 'label'] = 'Normal'
	label = 1
	primary_type = {"Normal":0}
	for i,da in enumerate(df['cases.0.project.primary_site']):
		if(df['cases.0.samples.0.sample_type'][i].find("Normal") >= 0):
			data['label'][i] = 0
		else:
			try:
				data['label'][i] = primary_type[df['cases.0.project.primary_site'][i]]
			except KeyError:
				primary_type[df['cases.0.project.primary_site'][i]] = label
				data['label'][i] = label
				label = label+1
	return primary_type,data

if __name__ == '__main__':


	data_dir =".."
	dirname = os.path.join(data_dir,"data");
	label_file = os.path.join(data_dir,"res","files_meta.tsv")
	
	#output file
	outputfile = os.path.join(data_dir ,"res","RNA_matrix")

	# extract data
	chunksize = 1000
	primary_type,label_df = extractLabel(label_file)
	with open(os.path.join(data_dir,"res",'Labels.json'), 'w') as fp:
		json.dump(primary_type, fp)
	print("Extracted all labels and stored in Label.json")
	for i in range(5):
		matrix_df = extractMatrix(dirname,i,chunksize)
		result = pd.merge(matrix_df, label_df, on='file_id', how="left")
		result.to_csv(outputfile+"-"+str(i)+".csv", index=False)
		print("Done for "+str(i+1)+"000 files")

 




