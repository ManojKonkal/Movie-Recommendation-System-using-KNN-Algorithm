document.getElementById("recommend-form").addEventListener("submit", async function (e) {
    e.preventDefault();
    const title = document.getElementById("movie-input").value;
    const sortBy = document.getElementById("sort-options").value;
  
    const response = await fetch("http://127.0.0.1:5000/recommend", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title })
    });
  
    const data = await response.json();
    const list = document.getElementById("recommendation-list");
    list.innerHTML = "";
  
    let recommendations = data.recommendations.map(name => ({
      name,
      year: 2000 + Math.floor(Math.random() * 24),
      rating: (Math.random() * 2 + 3).toFixed(1),
      votes: Math.floor(Math.random() * 1000000),
    }));
  
    if (sortBy === "rating") {
      recommendations.sort((a, b) => b.rating - a.rating);
    } else if (sortBy === "year") {
      recommendations.sort((a, b) => b.year - a.year);
    } else if (sortBy === "votes") {
      recommendations.sort((a, b) => b.votes - a.votes);
    }
  
    recommendations.forEach(movie => {
      const li = document.createElement("li");
      li.innerHTML = `
        <div class="movie-card">
          <div class="movie-details">
            <h3>${movie.name}</h3>
            <p><strong>Year:</strong> ${movie.year}</p>
            <p><strong>Rating:</strong> ⭐ ${movie.rating} / 5</p>
            <p><strong>Votes:</strong> ${movie.votes.toLocaleString()}</p>
          </div>
        </div>
      `;
      list.appendChild(li);
    });
  });
  