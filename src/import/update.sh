# These updates data files for back up
# If you are using the script, please use a repository for 
# the backing up of your dotfiles

#backs up configs to res folder
function backup {
	for i in ~/.*
	do
		if [ -f $i ]; then
			file=$(basename "${i}" | sed 's/.//' )
	 		cp $i res/$file
		fi	
	done
}
# restores saved configs in res
function restore {
	for i in res/*
	do 	
		base='.'$(basename "${i}")
		cp $i ~/$base
	done
}


while [ 1 == 1 ]
do
	echo "Do you want to backup or restore your configs? (r/b)"
	read P
	case "$P" in 
		"r") restore && break ;;
		"b") backup && break ;;
		*) echo "try again" ;;
	esac
done	

echo "Finished :)"
