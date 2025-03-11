<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Formulaire de connexion</title>
</head>
<body>
    <h2>Connexion</h2>
    <form action="/login" method="POST" id="login-form">
        <label for="username">Nom d'utilisateur :</label>
        <input type="text" id="username" name="username" required><br><br>
        
        <label for="password">Mot de passe :</label>
        <input type="password" id="password" name="password" required><br><br>
        
        <button type="submit">Se connecter</button>
    </form>

    <script>
        // Lors de la soumission du formulaire, nous évitons le comportement par défaut (rechargement de la page) et envoyons les données en AJAX.
        document.getElementById("login-form").addEventListener("submit", function(event) {
            event.preventDefault();

            var formData = new FormData(this);

            fetch("/login", {
                method: "POST",
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.access_token) {
                    // Si un jeton est renvoyé, on le stocke dans un cookie
                    document.cookie = `access_token=${data.access_token}; path=/;`;
                    alert("Connexion réussie !");
                    window.location.href = "/protected";  // Rediriger vers la route protégée
                } else {
                    alert("Erreur de connexion.");
                }
            })
            .catch(error => {
                alert("Erreur : " + error);
            });
        });
    </script>
</body>
</html>
