# info: create file with the pre and post vdj recombination results; 5 samples

len=100
samples=5

for i in $(seq 1 1 $samples)
do
    sonia-generate --humanTRB -n $len --pre -o "preTest$i.txt"
    sonia-generate --humanTRB -n $len --post -o "postTest$i.txt"
done
