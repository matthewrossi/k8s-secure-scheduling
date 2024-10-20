#!/bin/bash

set -e # make sure the job fails if any instruction fails

# Set current node region label
declare -a EU_REGIONS=("francecentral" "francesouth" "germanynorth" "germanywestcentral" "italynorth" "northeurope" "norwayeast" "norwaywest" "polandcentral" "spaincentral" "swedencentral" "switzerlandnorth" "switzerlandwest" "westeurope" "eu-central-1" "eu-central-2" "eu-north-1" "eu-south-1" "eu-south-2" "eu-west-1" "eu-west-3" "europe-central2" "europe-north1" "europe-southwest1" "europe-west1" "europe-west3" "europe-west4" "europe-west6" "europe-west8" "europe-west9" "europe-west12")
declare -a US_REGIONS=("centralus" "centraluseuap" "centralusstage" "eastus" "eastus2" "eastus2euap" "eastus2stage" "eastusstage" "eastusstg" "northcentralus" "northcentralusstage" "southcentralus" "southcentralusstage" "southcentralusstg" "westcentralus" "westus" "westus2" "westus2stage" "westus3" "westusstage" "us-east-1" "us-east-2" "us-gov-east-1" "us-gov-west-1" "us-west-1" "us-west-2" "us-central1" "us-east1" "us-east4" "us-east5" "us-south1" "us-west1" "us-west2" "us-west3" "us-west4")
# declare -a REGIONS=(${EU_REGIONS[${RANDOM} % 31]} ${US_REGIONS[${RANDOM} % 35]})
declare -a REGIONS=(${EU_REGIONS[@]} ${US_REGIONS[@]})

echo "${EU_REGIONS[@]}" | wc
echo "${US_REGIONS[@]}" | wc
echo ${REGIONS[@]} | wc
