#!/bin/bash

# Check if the input BAM file is provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 <input_bam_file>"
    exit 1
fi

input_bam_file=$1
temp_file="temp_output.txt"
output_file="output.txt"

# Check if the input file exists
if [ ! -f $input_bam_file ]; then
    echo "Error: Input BAM file not found"
    exit 1
fi

# Get the basename of the input BAM file
bam_basename=$(basename "$input_bam_file" .bam)

# Set the output directory
output_dir="/seq/vgb/chusted/SamToFastq/$bam_basename"

# Empty the temporary output file or create it if it doesn't exist
> $temp_file

# Execute samtools command, add the basename to the output, and append it to the temporary output file
samtools view -H "$input_bam_file" | grep '^@RG' | awk -v basename="$bam_basename" -v output_dir="$output_dir" '{ for (i=1;i<=NF;i++) { if ($i ~ /^ID:/) { sub(/^ID:/,"",$i); id=$i; } else if ($i ~ /^LB:/) { sub(/^LB:/,"",$i); lb=$i } } printf "%s\t%s\t$
    
# Empty the final output file or create it if it doesn't exist
> $output_file

# Read each line of the temporary output file, duplicate it, and append it to the final output file
while read -r line; do
    echo "$line" >> $output_file
    echo "$line" >> $output_file
done < "$temp_file"

# Clean up the temporary file
rm $temp_file
