# Run kubectl get pods -o wide and store the output
$podsOutput = kubectl get pods -o wide

# Split the output by newline characters
$pods = $podsOutput -split "`n"

# Remove the header line
$pods = $pods | Select-Object -Skip 1

# Iterate over each line to extract pod names
foreach ($podLine in $pods) {
    # Split the line by whitespace characters
    $podInfo = $podLine -split "\s+"
    
    # Extract the pod name (assuming it's in the first column)
    $podName = $podInfo[0]

    $podName
    # Run kubectl logs -f for each pod in a separate command prompt process
    Start-Process -FilePath "cmd.exe" -ArgumentList "/c kubectl logs -f $podName"

    Start-Sleep -Seconds 1

    
}
