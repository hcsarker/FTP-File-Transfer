/* =====================================================================
	 Global Frontend Logic for FTP File Transfer Demo
	 ---------------------------------------------------------------------
	 Responsibilities:
	 - Server start/stop buttons (TCP & UDP)
	 - File upload handling (detect page type by URL)
	 - Refresh received file list
	 - Minimal status badge updates
	 - Shared utility helpers
	 --------------------------------------------------------------------- */

document.addEventListener('DOMContentLoaded', () => {
	const path = window.location.pathname;

	// Utility helpers ---------------------------------------------------
	const qs = (sel, ctx=document) => ctx.querySelector(sel);
	const qsa = (sel, ctx=document) => Array.from(ctx.querySelectorAll(sel));
	const jsonFetch = (url, opts={}) => fetch(url, opts).then(r => r.json());

	// Determine protocol type based on current path --------------------
	const isTCPPage = path.includes('connection-oriented');
	const isUDPPage = path.includes('connectionless');

	// Status element (only present on protocol pages) ------------------
	const statusEl = qs('#serverStatus');
	function updateStatus(type, msg) {
		if (!statusEl) return;
		statusEl.textContent = msg;
		statusEl.className = 'status ' + (
			type === 'running' ? 'status-success' :
			type === 'error'   ? 'status-error'   : 'status-stopped'
		);
	}

	// Server controls ---------------------------------------------------
	qsa('[data-action][data-server]').forEach(btn => {
		btn.addEventListener('click', () => {
			const { action, server } = btn.dataset;
			const endpoint = (action === 'start') ?
				(server === 'co' ? '/start_co_server' : '/start_cl_server') :
				(server === 'co' ? '/stop_co_server' : '/stop_cl_server');
			jsonFetch(endpoint, { method: 'POST' })
				.then(data => {
					if (data.status === 'success') {
						const port = server === 'co' ? '2121' : '2122';
						updateStatus(action === 'start' ? 'running' : 'stopped', action === 'start' ? `Running (${port})` : 'Stopped');
					} else {
						updateStatus('error', 'Error: ' + data.message);
					}
				})
				.catch(err => updateStatus('error', 'Network Error: ' + err));
		});
	});

	// File upload -------------------------------------------------------
	const uploadForm = qs('#uploadForm');
	const fileInput = qs('#file');
	function resetDropLabel(){
		if(!fileInput) return;
		const lbl = fileInput.closest('.file-drop');
		const span = lbl ? lbl.querySelector('span') : null;
		if(span){
			span.textContent = isTCPPage ? 'Drop or select a file…' : isUDPPage ? 'Drop or select a text file…' : 'Select a file';
			lbl.classList.remove('has-file');
		}
	}
	if(fileInput){
		fileInput.addEventListener('change', () => {
			const lbl = fileInput.closest('.file-drop');
			const span = lbl ? lbl.querySelector('span') : null;
			if(span){
				if(fileInput.files && fileInput.files.length){
					span.textContent = fileInput.files[0].name;
					lbl.classList.add('has-file');
				} else {
					resetDropLabel();
				}
			}
		});
	}
	if (uploadForm) {
		uploadForm.addEventListener('submit', e => {
			e.preventDefault();
			const resultDiv = qs('#transferResult');
			const formData = new FormData(uploadForm);
			if (resultDiv) resultDiv.innerHTML = '<div class="loading">Sending file...</div>';
			const endpoint = isTCPPage ? '/send_co_file' : isUDPPage ? '/send_cl_file' : null;
			if (!endpoint) return;
			jsonFetch(endpoint, { method: 'POST', body: formData })
				.then(data => {
					if (resultDiv) {
						resultDiv.innerHTML = data.status === 'success'
							? `<div class="success">${data.message}</div>`
							: `<div class="error">${data.message}</div>`;
					}
					if(data.status === 'success'){resetDropLabel(); if(uploadForm) uploadForm.reset();}
					refreshFileList();
				})
				.catch(err => {
					if (resultDiv) resultDiv.innerHTML = `<div class="error">Error: ${err}</div>`;
				});
		});
	}

	// File list refresh -------------------------------------------------
	const fileListContainer = qs('#fileList');
	const refreshBtn = qs('#refreshFiles');
	function refreshFileList() {
		if (!fileListContainer) return;
		jsonFetch('/list_files')
			.then(data => {
				const arr = isTCPPage ? data.connection_oriented : isUDPPage ? data.connectionless : [];
				if (!arr || arr.length === 0) {
					fileListContainer.innerHTML = '<p class="empty">No files yet.</p>';
				} else {
					fileListContainer.innerHTML = '<ul>' + arr.map(f => `<li>${f}</li>`).join('') + '</ul>';
				}
			})
			.catch(() => {
				fileListContainer.innerHTML = '<p class="empty">Failed to load files.</p>';
			});
	}
	if (refreshBtn) refreshBtn.addEventListener('click', refreshFileList);

	// Initial list load if relevant
	if (fileListContainer) refreshFileList();

	// Theme toggle ------------------------------------------------------
	const themeBtn = qs('#themeToggle');
	function applyTheme(mode){
		const b = document.body;
		if(mode==='light'){b.classList.add('theme-light');} else {b.classList.remove('theme-light');}
		localStorage.setItem('ftpTheme', mode);
		if(themeBtn) themeBtn.textContent = mode==='light' ? '🌙 Dark' : '🌓 Light';
	}
	const savedTheme = localStorage.getItem('ftpTheme') || 'dark';
	applyTheme(savedTheme);
	if(themeBtn){
		themeBtn.addEventListener('click', () => {
			const next = document.body.classList.contains('theme-light') ? 'dark' : 'light';
			applyTheme(next);
		});
	}
});

