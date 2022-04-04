#! /bin/bash

VERSION=3.4.1
BINARY=yq_linux_amd64
SHA256SUM="adbc6dd027607718ac74ceac15f74115ac1f3caef68babfb73246929d4ffb23c"
DESTINATION="/home/jeffs/.local/bin"

# test if we need yq at all?  Create a calibrated yaml file
if test -e test.yaml; then
  echo "test.yaml already exists; cowardly unwilling to overwrite it"
  exit 1
cat - <<EOF >test.yaml
AWSTemplateFormatVersion: 2010-09-09
Metadata:
  'AWS::CloudFormation::Designer':
    fce72dbc-35c2-4ee7-9967-d29b9b654cc9:
      size:
        width: 140
        height: 140
      position:
        x: 154.00390625
        'y': 95.01171875
      z: 0
      embeds: []
    3d0c680b-30cf-4bef-863b-cd0a35ce50f3:
      size:
        width: 60
        height: 60
      position:
        x: 330
        'y': 130
      z: 0
      embeds: [A, B, C, 1]
      dependson:
        - fce72dbc-35c2-4ee7-9967-d29b9b654cc9
        - ffffeeee-dddd-cccc-bbbb-aaaaaaaaaaaa
        - fce72dbc-4ee7-35c2-bbbb-aaaaaaaaaaaa
EOF
# I suppose I could do something more sophisticated here, but that would be
# overthinking the problem.
if yq r -C test.yaml; then
  echo "yq is already present: $(whereis yq)"
  rm test.yaml
  exit 0

SAVED_IFS=$IFS



wget https://github.com/mikefarah/yq/releases/download/${VERSION}/${BINARY} -O ${DESTINATION}/yq
chmod a+x ${DESTINATION}/yq
sum256=$(sha256sum ${DESTINATION}/yq)                   # Answer is a string
sum256=($sum256)                                        # Convert to an array
sum256=${sum256[0]}                                     # grab one element in array
if test "$SHA256SUM" != "$sum256"; then
  echo "yq was not downloaded correctly: sha256sum is $sum256, should be $SHA256SUM"
  exit 1
else
  echo "yq downloaded okay.  Checksum check passed"
fi
if test "$(which yq)" != "${DESTINATION}/yq"; then
  echo "yq is not where it is supposed to be: $(which yq) is where it is, ${DESTINATION}/yq is where it should be"
  exit 1
else
  echo "yq is in ${DESTINATION}/yq where it belongs"
fi
  

echo "That should have looked nice"
exit 1

