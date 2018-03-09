function setUnit(unit){
  //change the sentence in result
  document.getElementById('unit').innerHTML="You select to use "+unit+" units";
  //change the value in table
  if(unit=="SI"){
    document.getElementById('unit_t1').innerHTML="(m)";
    document.getElementById('unit_t2').innerHTML="(m)";
    document.getElementById('unit_t3').innerHTML="(m^3)";
  }else{
    document.getElementById('unit_t1').innerHTML="(ft)";
    document.getElementById('unit_t2').innerHTML="(ft)";
    document.getElementById('unit_t3').innerHTML="(ft^3)";
  }
}

function setShape(shape){
  //change the sentence in result
  document.getElementById('shape').innerHTML="You selected to find the volume of "+shape;
  //change the value in table
  document.getElementById('shape_t').innerHTML=shape;
  //reset volume
  setVolume('');
  //enable or disable the height
  if(shape == 'Sphere'){
    document.getElementById('heightText').disabled = true;
    document.getElementById('heightText').value='';
    setHeight('N/A');
  }else{
    document.getElementById('heightText').disabled = false;
    if(document.getElementById('height').innerHTML == 'N/A'){
      setHeight('');
    }
  }
}

function resetForm(){
  //reset the form
  document.getElementById("myForm").reset();
  //reset the table
  setUnit('English');
  setShape('Cylinder');
  setRadius('');
  setHeight('');
}

//todo check data type
function setRadius(value) {
  //change the value in table
  document.getElementById('radius').innerHTML=value;
  setVolume('');
}

function setHeight(value){
  //change the value in table
  document.getElementById('height').innerHTML=value;
  setVolume('');
}

function calc(){
  var shapeToCalc=document.getElementById('shape_t').innerHTML;
  var vol = 0;
  var PI = 3.141592653;
  var r = document.getElementById('radius').innerHTML;
  var h = document.getElementById('height').innerHTML;
  if(shapeToCalc == 'Cylinder'){
      vol = PI*r*r*h;
  } else if (shapeToCalc == 'Sphere') {
      vol = PI*r*r*r*4/3;
  } else if (shapeToCalc == 'Cone') {
      vol = PI*r*r*h/3;
  }
  setVolume(vol);
}

function setVolume(value){
  document.getElementById('volume').innerHTML=value;
}
