var table = document.getElementsByTagName('tbody')[0];

var updateInput = document.getElementById("wordText");
var wordDefiition = document.getElementById("def");
var updateButton = document.getElementById("update");
var addButton = document.getElementById("add");

var modalCloses = document.getElementsByClassName("close");
var modelOpen = document.getElementsByClassName("open")[0];

var wordSearchButton = document.getElementById('search-button');
var wordSearchInput = document.getElementById('search-words');

var theme = document.getElementById("theme");

updateButton.disabled = true;
addButton.disabled = true;

wordSearchButton.addEventListener("click",searchWords);

wordSearchInput.addEventListener("change",searchWords);

updateInput.addEventListener("change",updateState);

updateButton.addEventListener("click",updateWord);

addButton.addEventListener("click",addWord);

theme.addEventListener("click",toggleTheme);

modalCloses[0].addEventListener("click",clearModal);

modalCloses[1].addEventListener("click",clearModal);

function searchWords(){
	word = wordSearchInput.value;
	
	$.get(`/find?word=${word}`,(res,code)=>{
		updateTable(JSON.parse(res));
	})
}

function updateTable(data) {

	clearTable();

	for (var i = 0; i < data.length; i++) {

		var row = document.createElement("TR")
		if(i%2==0) row.setAttribute("class","data-row even-row")
		else row.setAttribute("class","data-row odd-row")

		var word = document.createElement("TD");
		word.setAttribute("class","word");
		word.innerText = data[i].word;
		row.appendChild(word)

		var def = document.createElement("TD");
		def.setAttribute("class","def");
		def.innerText = data[i].definition;
		row.appendChild(def)

		var action = document.createElement("TD");
		action.setAttribute("class","action");
		action.setAttribute("data-word",data[i].word);
		
		var edit = document.createElement("i");
		edit.setAttribute("class","fas fa-edit");
		edit.addEventListener("click",editWord);
		action.appendChild(edit);

		var del = document.createElement("i");
		del.setAttribute("class","fas fa-trash-alt");
		del.addEventListener("click",deleteWord);
		action.appendChild(del);
		
		row.appendChild(action)

		table.appendChild(row)
	}
}

function clearTable(){
	var rows = document.getElementsByClassName("data-row");
	while(document.getElementsByClassName("data-row").length > 0) {
		document.getElementsByClassName("data-row")[0].remove();
	}
}

function editWord(e){
	word = e.target.parentElement.dataset.word;
	updateInput.value = word;
	updateState()
	modelOpen.click();
}

function deleteWord(e){
	word = e.target.parentElement.dataset.word;
	console.log(`deleting ${word}`);
	$.get(`/delete?word=${word}`,(res,code)=>{
		if(res.success) searchWords();
		else alert(res.error);
	})
}


function updateState() {
	word = updateInput.value;
	$.get(`/find?word=${word}&regex=False`,(res,code)=>{
		res = JSON.parse(res)
		if(res.length){
			wordDefiition.value = res[0].definition;
			updateButton.disabled = false;
			addButton.disabled = true;
		}
		else{
			wordDefiition.value = "";
			updateButton.disabled = true;
			addButton.disabled = false;
		}
	})
}

function addWord(){
	data = {
		'word' : updateInput.value,
		'definition' : wordDefiition.value 
	};

	if(data.definition == ""){
		alert("definition is empty");
		return;
	}

	$.post("/add",data,(res,code)=>{
		if(res.error) alert(res.error);
		else {
			modalCloses[0].click();
			alert(res.success)
		}
	})
}

function updateWord(){
	data = {
		'word' : updateInput.value,
		'definition' : wordDefiition.value 
	};

	if(data.definition == ""){
		alert("definition is empty");
		return;
	}

	$.post("/update",data,(res,code)=>{
		if(res.error) alert(res.error);
		else {
			modalCloses[0].click();
			alert(res.success);
		}
	})
}

function clearModal(argument) {
	updateInput.value = "";
	wordDefiition.value = "";
	addButton.disabled = true;
	updateButton.disabled = true;
	searchWords();
}

function toggleTheme(argument) {
	document.body.classList.toggle("dark-theme");
	theme.classList.toggle("fa-cloud-moon");
	theme.classList.toggle("fa-sun");
}

searchWords();

