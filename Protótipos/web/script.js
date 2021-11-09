document.querySelectorAll('[nav]').forEach(link =>{
			const conteudo = document.getElementById('conteudo')

			link.onclick = function(e) {
				e.preventDefault()
				/* Vai pegar o site do atributo wm-nav*/
				fetch(link.getAttribute('nav'))
					.then(resp => resp.text())
					.then(html => conteudo.innerHTML = html)
			}
		})

