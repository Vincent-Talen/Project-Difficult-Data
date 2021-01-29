echo 'Now installing fastqc'
sudo apt-get install fastqc;
echo 'Done installing fastqc, installing hisat2'
sudo apt-get install hisat2;
echo 'Done installing hisat2, installing cutadapt'
sudo apt-get install cutadapt;
echo 'Done installing cutadapt, installing samtools'
sudo apt-get install samtools;
echo 'Done installing samtools, installing required python packages'
sudo pip install -r requirements.txt
echo 'Done installing everything that is needed for the pipeline'