chrome.extension.onRequest.addListener(function(prediction){
    if (prediction==1){
        alert("Warning: Malicious website detected !!  SQL injections or Malware attacks might be expected !!");
        alert("Precaution: \n 1. Check the SSL Certificate \n 2. Look for the Website Trust Seal \n 3. Evaluate the Site with Security Tools \n 4. Check the URL");
    }else if (prediction==-1){
        alert("Keep going .... It's SAFE!!!");
    }
});