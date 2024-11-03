document.getElementById('contact-form').addEventListener('submit', function(event) { //  Ajout d'un écouteur d'événement sur le formulaire de contact
  event.preventDefault();
  const formData = new FormData(this);
  const url = this.getAttribute('data-url');  // Récupère l'attribut data-url du formulaire

  fetch(url, {//  Envoi de la requête au server sur l'url récupéré      
      method: 'POST',
      body: formData,
      headers: {
          'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value //   Envoi du token CSRF
      }
  })
  .then(response => { //  Envoi du server sur l'url récupéré et récupération du texte de la réponse
      if (response.ok) { // Envoi du server sur l'url récupéré et récupération du texte de la réponse
          return response.text();
      } else {
          return Promise.reject('Erreur lors de l\'envoi du formulaire');
      }
  })
  .then(responseText => {
      document.getElementById('message').style.display = 'block';//  Affichage du message de confirmation
      this.reset();
  })
  .catch(error => {
      console.error('Error:', error);
      alert('Une erreur est survenue lors de l\'envoi du formulaire. Veuillez réessayer.');
  });
});
