// Variable globale pour référencer le graphique
let myChart;

// Gestionnaire d'événement pour le chargement des données
document.getElementById('loadData').addEventListener('click', function() {
    // Effectuer une requête pour obtenir des données depuis le serveur
    fetch('/get_data')
        .then(response => response.json()) // Convertir la réponse en JSON
        .then(data => {
            createChart(data); // Créer ou mettre à jour le graphique avec les nouvelles données
        });
});

// Gestionnaire d'événement pour la recherche
document.getElementById('searchForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Empêcher le rechargement de la page lors de la soumission du formulaire
    const searchTerm = document.getElementById('searchTerm').value; // Avoir de la possibilité de rechercher un terme, puis qu'il soit afficher seul sur le graphique

    // Envoyer une requête avec le terme de recherche
    fetch(`/get_data?term=${encodeURIComponent(searchTerm)}`)
        .then(response => response.json()) // Convertir la réponse en JSON
        .then(data => {
            createChart(data); // Créer ou mettre à jour le graphique avec les données filtrées
        });
});

// Gestionnaire d'événement pour réinitialiser le zoom du graphique
document.getElementById('resetZoom').addEventListener('click', function() {
    if (myChart) {
        myChart.resetZoom(); // Réinitialiser le zoom si le graphique existe
    }
});

// Fonction pour créer un graphique
function createChart(data) {
    const ctx = document.getElementById('vocabChart').getContext('2d'); // Obtenir le contexte de dessin du canvas
    // Préparation des données pour le graphique
    const labels = data.map(v => v.Terme);
    const poidsAvance = data.map(v => v.PoidsAvance);
    const poidsIntermediaire = data.map(v => v.PoidsIntermediaire);
    const poidsDebutant = data.map(v => v.PoidsDebutant);

    if (myChart) {
        myChart.destroy(); // Détruire le graphique précédent si existant, pour revenir aux données de bae
    }

    // Création des différents grahiques à barres
    myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Avancé',
                data: poidsAvance,
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1
            }, {
                label: 'Intermédiaire',
                data: poidsIntermediaire,
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }, {
                label: 'Débutant',
                data: poidsDebutant,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true // Démarrer l'axe Y à zéro
                }
            },
            plugins: {
                zoom: {
                    zoom: {
                        wheel: {
                            enabled: true, // Activer le zoom avec la molette de la souris
                        },
                        pinch: {
                            enabled: true, // Activer le zoom avec le pincement (pour les appareils tactiles)
                        },
                        mode: 'xy' // Zoom sur les axes 'x' et 'y'
                    }
                }
            }
        }
    });
}
