function init() {

	var hash = document.location.hash;
	var res = hash.match(/t=([0-9]+)/);
	if (res) {
		var vids = document.getElementsByTagName('video');
		// only first video
		var vid = vids[0];
		vid.currentTime = res[1];
			vid.autoplay = true;
	}
}

init();

function vidTimeInUrl(el) {
	var vids = document.getElementsByTagName('video');
	// only first video
	var vid = vids[0];
	var currentTime = vid.currentTime;
	var href = el.href + "#t=" + parseInt(currentTime);
	el.href = href;
	return true;
}
