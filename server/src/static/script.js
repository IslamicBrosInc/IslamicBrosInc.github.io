document.addEventListener("DOMContentLoaded", function () {
  //ALL THIS IS MODAL STUFF
  // Get the modal
  var modal = document.getElementById("tmgan");

  // Get the button that opens the modal
  var btn = document.getElementsByClassName("box");

  // Get the <span> element that closes the modal
  var span = document.getElementsByClassName("close")[0];

  // When the user clicks the button, open the modal
  btn.onclick = function () {
    modal.style.display = "block";
  };

  // When the user clicks on <span> (x), close the modal
  span.onclick = function () {
    modal.style.display = "none";
  };

  // When the user clicks anywhere outside of the modal, close it
  window.onclick = function (event) {
    if (event.target == modal) {
      modal.style.display = "none";
    }
  };

  var modals = document.getElementsByClassName("modal");
  var btns = document.getElementsByTagName("button");
  var spans = document.getElementsByClassName("close");

  for (var i = 0; i < btns.length; i++) {
    (function (index) {
      btns[index].onclick = function () {
        modals[index].style.display = "block";
      };

      spans[index].onclick = function () {
        modals[index].style.display = "none";
      };
    })(i);
  }

  window.onclick = function (event) {
    for (var i = 0; i < modals.length; i++) {
      if (event.target === modals[i]) {
        modals[i].style.display = "none";
      }
    }
  };
  // END MODAL STUFF


//START SEARCH STUFF
  // Get the search form and search input field
  const searchForm = document.getElementById("search-form");
  const searchInput = document.getElementById("search-input");
  const resultsContainer = document.querySelector(".card-container");

  // Add an event listener to the search form for form submission
  searchForm.addEventListener("submit", function (event) {
    event.preventDefault();
    const query = searchInput.value.trim();

    fetch("/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query: query }),
    })
      .then((response) => response.json())
      .then((data) => {
        resultsContainer.innerHTML = ""; // Clear previous search results

        if (data.length === 0) {
          resultsContainer.innerHTML = "<p>No results found.</p>";
        } else {
          data.forEach((card) => {
            // Create HTML elements to display each search result card
            const cardDiv = document.createElement("div");
            cardDiv.classList.add("card");
            const titleHeading = document.createElement("h3");
            titleHeading.textContent = card.title;
            const descriptionPara = document.createElement("p");
            descriptionPara.textContent = card.transcript;

            cardDiv.appendChild(titleHeading);
            cardDiv.appendChild(descriptionPara);
            resultsContainer.appendChild(cardDiv);
          });
        }
      })
      .catch((error) => console.error("Error performing search:", error));
  });

  // ... Your existing modal and other JavaScript code ...
});
