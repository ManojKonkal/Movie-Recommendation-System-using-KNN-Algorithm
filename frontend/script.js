let allRecommendations = [];

document.getElementById("recommend-form").addEventListener("submit", function (e) {
  e.preventDefault();
  fetchRecommendations();
});

document.getElementById("genre-select").addEventListener("change", fetchRecommendations);
document.getElementById("sort-select").addEventListener("change", fetchRecommendations);

async function fetchRecommendations() {
  const language = document.getElementById("language-input").value.trim();
  const genre = document.getElementById("genre-select").value;
  const sortBy = document.getElementById("sort-select").value;

  if (!language) {
    alert("Please enter a language first.");
    return;
  }

  try {
    const response = await fetch("http://127.0.0.1:5000/recommend", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ language, genre, sort_by: sortBy })
    });

    const data = await response.json();
    allRecommendations = data.recommendations || [];
    renderRecommendations(sortBy);
  } catch (error) {
    console.error("Error fetching recommendations:", error);
  }
}

function renderRecommendations(sortBy) {
  const list = document.getElementById("recommendation-list");
  list.innerHTML = "";

  if (allRecommendations.length === 0) {
    list.innerHTML = "<p>No movies found for this selection.</p>";
    return;
  }

  // Optional: sort client-side (if backend doesn’t sort)
  if (sortBy === "rating") {
    allRecommendations.sort((a, b) => b["rating(10)"] - a["rating(10)"]);
  } else if (sortBy === "votes") {
    allRecommendations.sort((a, b) => b.votes - a.votes);
  } else if (sortBy === "name") {
    allRecommendations.sort((a, b) => a["movie name"].localeCompare(b["movie name"]));
  }

  allRecommendations.forEach(movie => {
    const li = document.createElement("li");
    li.innerHTML = `
      <div class="movie-card">
        <h3>${movie["movie name"]}</h3>
        <p>⭐ Rating: ${movie["rating(10)"]} / 10</p>
        <p>👍 Votes: ${movie["votes"].toLocaleString()}</p>
        <p>🎭 Genre: ${movie["genre"]}</p>
      </div>
    `;
    list.appendChild(li);
  });
}
