document.getElementById('contact-form').addEventListener('submit', function(event) {
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
  .then(response => {
      if (response.ok) {
          return response.text();
      } else {
          return Promise.reject('Erreur lors de l\'envoi du formulaire');
      }
  })
  .then(responseText => {
      document.getElementById('message').style.display = 'block';
      this.reset();
  })
  .catch(error => {
      console.error('Error:', error);
      alert('Une erreur est survenue lors de l\'envoi du formulaire. Veuillez réessayer.');
  });
});
