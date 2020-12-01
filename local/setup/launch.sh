yourfilenames=`ls ./*.yaml`
for eachfile in $yourfilenames
do
   kubectl apply -f $eachfile
done