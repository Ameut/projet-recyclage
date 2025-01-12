document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('demande-devis-form').addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(this);

        fetch('/demande-devis/', {// Envoi de la requête au server sur l'url récupéré
            method: 'POST',
            body: formData,// Envoi du token CSRF
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())// Envoi du server sur l'url récupéré et récupération du texte de la réponse
        .then(data => {
            let messageDiv = document.getElementById('message');// Récupération du message de confirmation
            if (data.success) {
                messageDiv.innerHTML = '<div class="alert alert-success">Votre demande de devis a été soumise avec succès !</div>';
            } else {
                messageDiv.innerHTML = '<div class="alert alert-danger">Il y a eu une erreur lors de la soumission de votre demande. Veuillez réessayer.</div>';
            }
        })
        .catch(error => {
            console.error('Erreur:', error);
            document.getElementById('message').innerHTML = '<div class="alert alert-danger">Une erreur est survenue. Veuillez réessayer plus tard.</div>';
        });
    });
});