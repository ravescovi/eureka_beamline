
mkdir ~/workspace_bits
cd ~/workspace_bits
mkdir base
cd base
git clone https://github.com/BCDA-APS/BITS
git clone https://github.com/BCDA-APS/BITS-Starter
git clone https://github.com/BCDA-APS/apstools
git clone https://github.com/spc-group/guarneri # to be moved into BCDA-APS
git clone https://github.com/spc-group/ophyd-registry # to be moved into BCDA-APS
git clone https://github.com/ravescovi/eureka_beamline
cd ..

mkdir deploy
cd deploy
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEPLOYMENTS_FILE="${SCRIPT_DIR}/deployments.json"

if [ ! -f "$DEPLOYMENTS_FILE" ]; then
    echo "No deployments found at ${DEPLOYMENTS_FILE}. Continuing without deployments..."
else
    echo "Reading deployments from ${DEPLOYMENTS_FILE}..."
    
    # Read deployments.json and clone each repository into its designated folder
    while IFS= read -r repo; do
        NAME=$(echo "$repo" | jq -r '.name')
        URL=$(echo "$repo" | jq -r '.url')
        echo "Cloning repository ${NAME} from ${URL}..."
        git clone "$URL" "$NAME"
    done < <(jq -c '.[]' "$DEPLOYMENTS_FILE")
fi

cd ..

