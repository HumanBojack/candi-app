document.querySelectorAll('.delete-btn').forEach(item => {
  item.addEventListener("click", onDeleteClick)
})
function onDeleteClick(e) {
  e.preventDefault()
  if (confirm('Etes-vous sur de vouloir supprimer la candidature?')) {
    location.replace(e.currentTarget.href)
  }
} 