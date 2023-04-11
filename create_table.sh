#!/bin/bash
source /broad/software/scripts/useuse
use UGER
use .samtools-1.9

# Check if the input BAM file is provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 <input_bam_file>"
    exit 1
fi

input_bam_file=$1
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

# Empty the final output file or create it if it doesn't exist
> $output_file

# Execute samtools command, create the desired output, and append it to the final output file
samtools view -H "$input_bam_file" | grep '^@RG' | awk -v basename="$bam_basename" -v output_dir="$output_dir" '{ for (i=1;i<=NF;i++) { if ($i ~ /^ID:/) { sub(/^ID:/,"",$i); id=$i; } else if ($i ~ /^LB:/$



