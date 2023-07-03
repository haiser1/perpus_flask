function liveSearch() {
    var input = document.getElementById("searchInput");
    var filter = input.value.toLowerCase();
    var results = document.getElementById("searchResults");
  
    // Hapus hasil pencarian sebelumnya
    results.innerHTML = "";
  
    // Kirim permintaan AJAX ke server-side
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        var searchResults = JSON.parse(this.responseText);
        searchResults.forEach(function(result) {
          var li = document.createElement("li");
          li.textContent = result;
          li.onclick = function() {
            input.value = result;
            results.innerHTML = "";
          };
          results.appendChild(li);
        });
      }
    };
    xmlhttp.open("POST", "/search" + filter, true);
    xmlhttp.send();
  }
  
  // Mengikat event 'keyup' pada input pencarian
  document.getElementById("searchInput").addEventListener("keyup", function() {
    liveSearch();
  });
  