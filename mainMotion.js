// D:\py\pythonProject

// https://gltf-viewer.donmccurdy.com/
// https://gltf.nsdt.cloud/
// morph targe: *****
// https://zhuanlan.zhihu.com/p/603831726
// https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html
import * as THREE from 'three';

import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { DRACOLoader } from 'three/addons/loaders/DRACOLoader.js';
import { FBXLoader } from 'three/addons/loaders/FBXLoader'
import { GLTFExporter } from "three/addons/exporters/GLTFExporter.js";
import {GUI} from 'three/addons/libs/lil-gui.module.min.js';
import * as R from 'myLib'
import {animArray}  from './array.js'


function getByItemName(animArray, name) {
  let ret = null;
  let len = animArray.length;
  for(let i=0; i<len; i++) {
      let item = animArray[i];
      if(item.name == name) {
        return item;
      }
  }
  return ret;
}

const one = new THREE.Vector3(1, 1, 1);
const zero = new THREE.Vector3(0, 0, 0);
function getByItemNameVectory(animArray, name, frameIdx, defaultValue) {
  let ret = getByItemName(animArray, name);
  if(ret== null) {
    return defaultValue;
  }
  let values = ret.values;
  let eleLen = values/3;
  let i = frameIdx;
  let item =  values[i*3+0];
  let item1 = values[i*3+1];
  let item2 = values[i*3+2];     
  return new THREE.Vector3(item, item1, item2);
}

function getByItemNameQuaternion(animArray, name, frameIdx) {
  let ret = getByItemName(animArray, name);
  if(ret== null) {
    return new THREE.Quaternion(1, 0, 0, 0);
  }
  let values = ret.values;
  let eleLen = values/3;
  let i = frameIdx;
  let item =  values[i*3+0];
  let item1 = values[i*3+1];
  let item2 = values[i*3+2];     
  let item3 = values[i*3+3];     
  return new THREE.Quaternion(item, item1, item2, item3);
}

function getMatrixByBoneName(animArray, name, frameIdx) {
  let ret0 = getByItemNameVectory(animArray, name+".position", frameIdx, zero);
  let ret1 = getByItemNameVectory(animArray, name+".scale", frameIdx, one);
  let ret2 = getByItemNameQuaternion(animArray, name+".quaternion", frameIdx, zero);
  let mat = new THREE.Matrix4();
  return mat.compose(ret0, ret2, ret1);
}

let ret = getMatrixByBoneName(animArray, "R_Forearm", 0);
console.log(ret)

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
let renderer = new THREE.WebGLRenderer({
  antialias: true,     //抗锯齿
  // alpha: true
})
const controls = new OrbitControls( camera, renderer.domElement );

renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(window.devicePixelRatio)

document.body.appendChild(renderer.domElement);
 
const geometry = new THREE.BoxGeometry(1, 1, 1);
const material = new THREE.MeshBasicMaterial({ color: 0x00ff00 });

let glbInfo = {
  "Name": "Casual-M-0052",
  "UrlName": "casual-m-0052",
  "Url": "https://actorcore-dl.reallusion.com/Signed/glb/webgl/JIC71c7722421cfc14b9/MainData/Type573440/casual-m-0052?Policy=ew0KICAiU3RhdGVtZW50IjogWw0KICAgIHsNCiAgICAgICJSZXNvdXJjZSI6ICJodHRwczovL2FjdG9yY29yZS1kbC5yZWFsbHVzaW9uLmNvbS9TaWduZWQvZ2xiL3dlYmdsL0pJQzcxYzc3MjI0MjFjZmMxNGI5L01haW5EYXRhL1R5cGU1NzM0NDAvY2FzdWFsLW0tMDA1MiIsDQogICAgICAiQ29uZGl0aW9uIjogew0KICAgICAgICAiRGF0ZUdyZWF0ZXJUaGFuIjogew0KICAgICAgICAgICJBV1M6RXBvY2hUaW1lIjogMTc0MDExMjQ4Mw0KICAgICAgICB9LA0KICAgICAgICAiRGF0ZUxlc3NUaGFuIjogew0KICAgICAgICAgICJBV1M6RXBvY2hUaW1lIjogMTc0MDExMjkwMw0KICAgICAgICB9DQogICAgICB9DQogICAgfQ0KICBdDQp9&Signature=BFCl2sKPT93zHW-0QiO62fK7NfIRPgBsUatL5rQ1tQBNkErDex5Wf6umsNW3mjAfhkK6ih5EEUTVL7QqpMOLkPvuXb9CfSyedk~bsTizxgJFNLzTDar94P1Wz2owvLmfqsOpoQ53pTszgZUmF3j5gfhQbuzEPd0klK0HI7f~HtBb2RLbokosKGpTUAgSrVsPYTu-ZiOy3Dk5ojlaT5MaHC1weuC203RlwqumDjydkBPFdE1ojImHVu0h0li4wKd46d83d54h1j2Zk8d6V044cXhYXNezjYb6W~E6NbWk8UjCGZzTo321KEGsa0nB8rmwqbKY-sj79pzL~4I-4dHl8Q__&Key-Pair-Id=APKAJTXU3U7NXSAXNPPA",
  "EInfo": "pzk6jZT9rtF8PYMWD4UK0xyonIvdwbA2",
  "VInfo": "LE5tkab3feRAZoWp",
  "DInfo": "GaSLIiAM5Wvx47w9tOPjBoJg1Ty2dVKD",
  "WInfo": "8CnexlrfIMwaUQ5N",
  "MInfo": "9bjxsCEhAMZ2t46fJ7o1OyzwHTeYLQUl",
  "MeshNodeName": null,
  "AvatarTexturePath": {
      "Metallic": null,
      "BaseColor": null,
      "Roughness": null,
      "Opacity": null,
      "Normal": null,
      "AO": null
  },
  "PremiumBaseID": "",
  "CustomTag": [
      "actorSCAN",
      "Elderly",
      "General",
      "Male"
  ],
  "Mesh": "{\"DJ1\":{\"Materials\":{\"Character\":{\"Material Type\":\"Pbr\",\"MultiUV Index\":0,\"Two Side\":true,\"Diffuse Color\":[255.0,255.0,255.0],\"Ambient Color\":[255.0,255.0,255.0],\"Specular Color\":[255.0,255.0,255.0],\"Opacity\":1.0,\"Self Illumination\":0.0,\"Textures\":{\"Metallic\":{\"Texture Path\":\"https://actorcore-dl.reallusion.com/Signed/glb/webgl/JIC71c7722421cfc14b9/MainData/Type573440/JIC71c7722421cfc14b9.fbm/Character_Metallic.jpg?Policy=ew0KICAiU3RhdGVtZW50IjogWw0KICAgIHsNCiAgICAgICJSZXNvdXJjZSI6ICJodHRwczovL2FjdG9yY29yZS1kbC5yZWFsbHVzaW9uLmNvbS9TaWduZWQvZ2xiL3dlYmdsL0pJQzcxYzc3MjI0MjFjZmMxNGI5L01haW5EYXRhL1R5cGU1NzM0NDAvSklDNzFjNzcyMjQyMWNmYzE0YjkuZmJtL0NoYXJhY3Rlcl9NZXRhbGxpYy5qcGciLA0KICAgICAgIkNvbmRpdGlvbiI6IHsNCiAgICAgICAgIkRhdGVHcmVhdGVyVGhhbiI6IHsNCiAgICAgICAgICAiQVdTOkVwb2NoVGltZSI6IDE3NDAxMTI0ODMNCiAgICAgICAgfSwNCiAgICAgICAgIkRhdGVMZXNzVGhhbiI6IHsNCiAgICAgICAgICAiQVdTOkVwb2NoVGltZSI6IDE3NDAxMTQ0MDMNCiAgICAgICAgfQ0KICAgICAgfQ0KICAgIH0NCiAgXQ0KfQ__&Signature=PAGdHKEaWKtj6jXM7hiyiHMGDel8uPsWXogIP5-pjcAVhOy2HzTgtdll-kWzOANAzZvErvDSuXvcRCcSw1NpQVwGtEE7k1aJO1zysUGHDkY7tpJP2Dz82J21lmGGn5AOOtHCYpURtGxRVfiYaeEyyH6HPkpd0zQsIGuVRUX8~nAemtV3Obs28pQvnbFav5IypXfOOwcz825W0HafWvo9nx639QAnIlYy6gzPNxQZ8UBWXbdmwVy05iQL10-N032w26PmLORkThlpqquu17lkZ5NYV3fHuqZKC-X7GHlK7MIbTIuanV8LbD-1MnMU5cReWeDv76gno75kFRGrxZhTPQ__&Key-Pair-Id=APKAJTXU3U7NXSAXNPPA\",\"Strength\":100.0,\"Offset\":[0.0,0.0],\"Tiling\":[1.0,1.0]},\"Diffuse\":{\"Texture Path\":\"https://actorcore-dl.reallusion.com/Signed/glb/webgl/JIC71c7722421cfc14b9/MainData/Type573440/JIC71c7722421cfc14b9.fbm/Character_Diffuse.png?Policy=ew0KICAiU3RhdGVtZW50IjogWw0KICAgIHsNCiAgICAgICJSZXNvdXJjZSI6ICJodHRwczovL2FjdG9yY29yZS1kbC5yZWFsbHVzaW9uLmNvbS9TaWduZWQvZ2xiL3dlYmdsL0pJQzcxYzc3MjI0MjFjZmMxNGI5L01haW5EYXRhL1R5cGU1NzM0NDAvSklDNzFjNzcyMjQyMWNmYzE0YjkuZmJtL0NoYXJhY3Rlcl9EaWZmdXNlLnBuZyIsDQogICAgICAiQ29uZGl0aW9uIjogew0KICAgICAgICAiRGF0ZUdyZWF0ZXJUaGFuIjogew0KICAgICAgICAgICJBV1M6RXBvY2hUaW1lIjogMTc0MDExMjQ4Mw0KICAgICAgICB9LA0KICAgICAgICAiRGF0ZUxlc3NUaGFuIjogew0KICAgICAgICAgICJBV1M6RXBvY2hUaW1lIjogMTc0MDExNDQwMw0KICAgICAgICB9DQogICAgICB9DQogICAgfQ0KICBdDQp9&Signature=WYCqrtCZBk~iT8D7H4ud4028RUKEwMH4R0RWBOvCkW48jsrO0zOcgxQ8zoQODpczm7uBEoTw9nuQmq8q0mi5FePeBkaBEZhBHMG~kZ4kID9cIPUdsMNm0ayuluK2zuHa6U7DIn9BZTqzUpt3d4PqBSK5BCGh0RqYaMSr~-Ne8Z6a8Ml4yv5-cZgcV-4VW5EDT3U2T7OU~mA~QPw1cxLY9uk5mpUBqLsA~9snMqgfcZtND9on9iAavevlB0vQjHHbbENQP3veOh3YjHWkxhnMpjdcBoTKeJXX3h7n--Zw0rPzAYncHLFNj1txSP4nSbguVQ4Bffb~qdHKs7nIhVrfPw__&Key-Pair-Id=APKAJTXU3U7NXSAXNPPA\",\"Strength\":100.0,\"Offset\":[0.0,0.0],\"Tiling\":[1.0,1.0]},\"Roughness\":{\"Texture Path\":\"https://actorcore-dl.reallusion.com/Signed/glb/webgl/JIC71c7722421cfc14b9/MainData/Type573440/JIC71c7722421cfc14b9.fbm/Character_Roughness.jpg?Policy=ew0KICAiU3RhdGVtZW50IjogWw0KICAgIHsNCiAgICAgICJSZXNvdXJjZSI6ICJodHRwczovL2FjdG9yY29yZS1kbC5yZWFsbHVzaW9uLmNvbS9TaWduZWQvZ2xiL3dlYmdsL0pJQzcxYzc3MjI0MjFjZmMxNGI5L01haW5EYXRhL1R5cGU1NzM0NDAvSklDNzFjNzcyMjQyMWNmYzE0YjkuZmJtL0NoYXJhY3Rlcl9Sb3VnaG5lc3MuanBnIiwNCiAgICAgICJDb25kaXRpb24iOiB7DQogICAgICAgICJEYXRlR3JlYXRlclRoYW4iOiB7DQogICAgICAgICAgIkFXUzpFcG9jaFRpbWUiOiAxNzQwMTEyNDgzDQogICAgICAgIH0sDQogICAgICAgICJEYXRlTGVzc1RoYW4iOiB7DQogICAgICAgICAgIkFXUzpFcG9jaFRpbWUiOiAxNzQwMTE0NDAzDQogICAgICAgIH0NCiAgICAgIH0NCiAgICB9DQogIF0NCn0_&Signature=PKXGH8hGqO0zOmtKjgXHvBQXSC1RVj4tRNtflheFAcHKqykMF2YaM8tcKuyy~Gtmu4yQrWoLh9~LGeemBdKctZYxU2nGGJ~HQiN1ASR-1yI5j6cuZciMtng6Tp4MPU~n1V04muIuLRVTQ9pLABQr717WMMRQdhVwThZ3yEkHoH6jXCe3jEnX9lz2jhjv5RKTR1ZkGdUspykLUmo6eofzRTI9lLvR-BTQL3sWlHvyc5IP4KCp7gig9nFgzXRkhWIGKbUeRlZFlNyF-oIUKzCOC~aV3HE3JvHQEdALC8Dtd0EwKkbW9yKKDHuV9IaKkhG~w4jQtaaFZIKPIXRJ1oCrFg__&Key-Pair-Id=APKAJTXU3U7NXSAXNPPA\",\"Strength\":100.0,\"Offset\":[0.0,0.0],\"Tiling\":[1.0,1.0]},\"Glow\":{\"Texture Path\":\"https://actorcore-dl.reallusion.com/Signed/glb/webgl/JIC71c7722421cfc14b9/MainData/Type573440/JIC71c7722421cfc14b9.fbm/Character_Glow.jpg?Policy=ew0KICAiU3RhdGVtZW50IjogWw0KICAgIHsNCiAgICAgICJSZXNvdXJjZSI6ICJodHRwczovL2FjdG9yY29yZS1kbC5yZWFsbHVzaW9uLmNvbS9TaWduZWQvZ2xiL3dlYmdsL0pJQzcxYzc3MjI0MjFjZmMxNGI5L01haW5EYXRhL1R5cGU1NzM0NDAvSklDNzFjNzcyMjQyMWNmYzE0YjkuZmJtL0NoYXJhY3Rlcl9HbG93LmpwZyIsDQogICAgICAiQ29uZGl0aW9uIjogew0KICAgICAgICAiRGF0ZUdyZWF0ZXJUaGFuIjogew0KICAgICAgICAgICJBV1M6RXBvY2hUaW1lIjogMTc0MDExMjQ4Mw0KICAgICAgICB9LA0KICAgICAgICAiRGF0ZUxlc3NUaGFuIjogew0KICAgICAgICAgICJBV1M6RXBvY2hUaW1lIjogMTc0MDExNDQwMw0KICAgICAgICB9DQogICAgICB9DQogICAgfQ0KICBdDQp9&Signature=LZoNyYiwf4x0TTXJqDW3n2zBgEt5OH53ctvtVaVZ4MwnUZuqgN35N0CRgQVq-5H~MKTtAr1-vj~zriZDUrO~PqrOCPB-BA~XTtLcyLTID~HPoT5FGIqLr~lyAOJwvJMDSh3XPzmtQY7rsqN4LJ-FcwOBEsKKbTUl0PtVwUfMys7sNl~iMjdwpul4sCzjeZ6BcIiC7XADYfdCLotc15gcjJUbH2ao9KooltoA9nLZG-MOuq5AcHbsYBXv2q0GFU0sYcCryi-8sH-FqzuMzsQrIBGMnmGIwZexwg12vy9vno8cEW4WlQbhAKQ5407U4prCQhX9tVjsFqX2~Bb2QUHE0Q__&Key-Pair-Id=APKAJTXU3U7NXSAXNPPA\",\"Strength\":100.0,\"Offset\":[0.0,0.0],\"Tiling\":[1.0,1.0]},\"Opacity\":{\"Texture Path\":\"https://actorcore-dl.reallusion.com/Signed/glb/webgl/JIC71c7722421cfc14b9/MainData/Type573440/JIC71c7722421cfc14b9.fbm/Character_Diffuse.png?Policy=ew0KICAiU3RhdGVtZW50IjogWw0KICAgIHsNCiAgICAgICJSZXNvdXJjZSI6ICJodHRwczovL2FjdG9yY29yZS1kbC5yZWFsbHVzaW9uLmNvbS9TaWduZWQvZ2xiL3dlYmdsL0pJQzcxYzc3MjI0MjFjZmMxNGI5L01haW5EYXRhL1R5cGU1NzM0NDAvSklDNzFjNzcyMjQyMWNmYzE0YjkuZmJtL0NoYXJhY3Rlcl9EaWZmdXNlLnBuZyIsDQogICAgICAiQ29uZGl0aW9uIjogew0KICAgICAgICAiRGF0ZUdyZWF0ZXJUaGFuIjogew0KICAgICAgICAgICJBV1M6RXBvY2hUaW1lIjogMTc0MDExMjQ4Mw0KICAgICAgICB9LA0KICAgICAgICAiRGF0ZUxlc3NUaGFuIjogew0KICAgICAgICAgICJBV1M6RXBvY2hUaW1lIjogMTc0MDExNDQwMw0KICAgICAgICB9DQogICAgICB9DQogICAgfQ0KICBdDQp9&Signature=WYCqrtCZBk~iT8D7H4ud4028RUKEwMH4R0RWBOvCkW48jsrO0zOcgxQ8zoQODpczm7uBEoTw9nuQmq8q0mi5FePeBkaBEZhBHMG~kZ4kID9cIPUdsMNm0ayuluK2zuHa6U7DIn9BZTqzUpt3d4PqBSK5BCGh0RqYaMSr~-Ne8Z6a8Ml4yv5-cZgcV-4VW5EDT3U2T7OU~mA~QPw1cxLY9uk5mpUBqLsA~9snMqgfcZtND9on9iAavevlB0vQjHHbbENQP3veOh3YjHWkxhnMpjdcBoTKeJXX3h7n--Zw0rPzAYncHLFNj1txSP4nSbguVQ4Bffb~qdHKs7nIhVrfPw__&Key-Pair-Id=APKAJTXU3U7NXSAXNPPA\",\"Strength\":100.0,\"Offset\":[0.0,0.0],\"Tiling\":[1.0,1.0]},\"Normal\":{\"Texture Path\":\"https://actorcore-dl.reallusion.com/Signed/glb/webgl/JIC71c7722421cfc14b9/MainData/Type573440/JIC71c7722421cfc14b9.fbm/Character_Bump.jpg?Policy=ew0KICAiU3RhdGVtZW50IjogWw0KICAgIHsNCiAgICAgICJSZXNvdXJjZSI6ICJodHRwczovL2FjdG9yY29yZS1kbC5yZWFsbHVzaW9uLmNvbS9TaWduZWQvZ2xiL3dlYmdsL0pJQzcxYzc3MjI0MjFjZmMxNGI5L01haW5EYXRhL1R5cGU1NzM0NDAvSklDNzFjNzcyMjQyMWNmYzE0YjkuZmJtL0NoYXJhY3Rlcl9CdW1wLmpwZyIsDQogICAgICAiQ29uZGl0aW9uIjogew0KICAgICAgICAiRGF0ZUdyZWF0ZXJUaGFuIjogew0KICAgICAgICAgICJBV1M6RXBvY2hUaW1lIjogMTc0MDExMjQ4Mw0KICAgICAgICB9LA0KICAgICAgICAiRGF0ZUxlc3NUaGFuIjogew0KICAgICAgICAgICJBV1M6RXBvY2hUaW1lIjogMTc0MDExNDQwMw0KICAgICAgICB9DQogICAgICB9DQogICAgfQ0KICBdDQp9&Signature=YnTswuEda2Rz7-RJlZy52lHnM4~GTgQFFQdWej5TWrTCQtvpCL146imXlI0LcCpPt-aWxmVv6qjVi91~nCj~m9eey9xBHdJGvFLIdlgHEm465VNDLJVCRaoggzXfh7V6S~g3AQFWzVwFinX5alYaz0ZohDyoIxYHFT5mE6BBIP4j9ukwzXUSAKXfMYz7uddnLGLhC8kvBMtPtSTV9tDpa6jgRid9MC~uunN51ViyLSrbHE5VS6qyYR4YqtYc40HkyHQyVZFT~CTkoV5u~2L~6pnLNgVNvsmgSEaSboFkg2k0pJEAV0J2rEj2JsoKqJSPEgdSGtQsV40VLj~EOf0V6A__&Key-Pair-Id=APKAJTXU3U7NXSAXNPPA\",\"Strength\":100.0,\"Offset\":[0.0,0.0],\"Tiling\":[1.0,1.0]},\"AO\":{\"Texture Path\":\"https://actorcore-dl.reallusion.com/Signed/glb/webgl/JIC71c7722421cfc14b9/MainData/Type573440/JIC71c7722421cfc14b9.fbm/Character_AO.jpg?Policy=ew0KICAiU3RhdGVtZW50IjogWw0KICAgIHsNCiAgICAgICJSZXNvdXJjZSI6ICJodHRwczovL2FjdG9yY29yZS1kbC5yZWFsbHVzaW9uLmNvbS9TaWduZWQvZ2xiL3dlYmdsL0pJQzcxYzc3MjI0MjFjZmMxNGI5L01haW5EYXRhL1R5cGU1NzM0NDAvSklDNzFjNzcyMjQyMWNmYzE0YjkuZmJtL0NoYXJhY3Rlcl9BTy5qcGciLA0KICAgICAgIkNvbmRpdGlvbiI6IHsNCiAgICAgICAgIkRhdGVHcmVhdGVyVGhhbiI6IHsNCiAgICAgICAgICAiQVdTOkVwb2NoVGltZSI6IDE3NDAxMTI0ODMNCiAgICAgICAgfSwNCiAgICAgICAgIkRhdGVMZXNzVGhhbiI6IHsNCiAgICAgICAgICAiQVdTOkVwb2NoVGltZSI6IDE3NDAxMTQ0MDMNCiAgICAgICAgfQ0KICAgICAgfQ0KICAgIH0NCiAgXQ0KfQ__&Signature=Yffs6ZEyLyDSQF~wW0apKVSJJb8vwWs-7OybloeGKLeJQH3FqZ3Ypcep6iRsRYpS~0M8eLTedsmuJvebRLhXx1udy0qLdTvbllSxs0RrdHI8BmWM5NuMpN4gDWCxf6sBpKUmfAW0Vk8tk~gIspSrPErab4qLRdIomNJVP6qw4e54Cm-3wv56updxexsy~SFxZ8FpiR4-~0Z-wcCpQ3lL9CPIo0URXOtqGk8VMrDQjPRfHNnT-gZl86yQ4dyA-yufPXTnQ-bPXiFsb4dll6LNvT3Q61xWc8BAT5lQ61vOi~NentlHx3v-VKnFmXkYaoVmRsTcmw~q2yXmqlacKmDKpQ__&Key-Pair-Id=APKAJTXU3U7NXSAXNPPA\",\"Strength\":100.0,\"Offset\":[0.0,0.0],\"Tiling\":[1.0,1.0]}}}}}}",
  "AccessoryAttachInfo": null,
  "NeedConvertMotion": false,
  "ActorPoseOffset": null,
  "MaterialSet": {
      "Thumbnail": null,
      "JsonFileInfo": null
  },
  "PresetMotions": null,
  "DefaultEnvironment": 0,
  "FollowCamera": false,
  "ZeroRoot": false,
  "Mirror": false,
  "Grid": false,
  "Ground": false,
  "CameraInfos": null,
  "Status": 1,
  "AccessoryMotionInfo": {
      "DefaultAccessoryContents": null,
      "AccessoryListContents": null,
      "IsAnimatedAccessory": false
  }
};

function downloadFile(fileName, content) {
  // 定义触发事件的DOM
  var aLink = document.createElement('a');
  // 定义BLOB对象，声明文件内容
  var blob = new Blob([content, 'jyjin']);
  // 判定平台
  var isMac = navigator.userAgent.indexOf('Mac OS') > -1;
  // 定义事件对象 
  var evt = document.createEvent(isMac ? "MouseEvents" : "HTMLEvents");
  // 初始化事件
  // evt.initEvent("click", false, false);
  evt[isMac ? "initMouseEvent" : "initEvent"]("click", false, false);
  // 定义下载文件名称
  aLink.download = fileName;
  // 根据上面定义的 BLOB 对象创建文件 dataURL
  aLink.href = URL.createObjectURL(blob);
  // 触发事件下载
  aLink.dispatchEvent(evt);
}


const light2 = new THREE.AmbientLight(0xffffff, 1); // soft white light
scene.add(light2);

//直线光源
const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
directionalLight.position.set(10, 10, 10);
scene.add(directionalLight);

const textureLoader = new THREE.TextureLoader();

const texture = textureLoader.load('./Character_Diffuse.png');
const boxGeometry = new THREE.BoxGeometry(1, 1, 1);

const boxMaterial = new THREE.MeshStandardMaterial({
  color: 0xffffff,
  map: texture, // 2.重点位置
});
const boxMesh = new THREE.Mesh(boxGeometry, boxMaterial);

const cube2 = new THREE.Mesh(geometry, material);
camera.position.z = 5;
let texLoader = new THREE.TextureLoader()

function animate() {
    requestAnimationFrame(animate);
 
    renderer.render(scene, camera);
}
 
animate();


function drawLne(name, childName, point1, point2) {
  const materialLine = new THREE.LineBasicMaterial({
    color: 0x0000ff
  });

  if(name == "RootNode") {
    let SCALE = 0.02;
    const material = new THREE.MeshBasicMaterial({ color: 0xff0000, wireframe:true });
    const geometry = new THREE.BoxGeometry(SCALE, SCALE, SCALE);
    const cube = new THREE.Mesh(geometry, material);
    cube.position.x = point1.x;
    cube.position.y = point1.y;
    cube.position.z = point1.z;
    scene.add( cube );
  }else {
    const material = new THREE.MeshBasicMaterial({ color: 0x00ff00, wireframe:true });
      let SCALE = 0.01;
      const geometry = new THREE.BoxGeometry(SCALE, SCALE, SCALE);
      const cube = new THREE.Mesh(geometry, material);
      cube.position.x = point1.x;
      cube.position.y = point1.y;
      cube.position.z = point1.z;
      scene.add( cube );
  }

  const points = [];
  points.push( point1);
  points.push( point2 );
  const geometry2 = new THREE.BufferGeometry().setFromPoints( points );
  const line = new THREE.Line( geometry2, materialLine );
  scene.add( line );
}


function getMatrix(bone) {
  let mat = new THREE.Matrix4();
  mat = mat.premultiply(bone.matrix);
  let parent = bone.parent;
  while(parent!= null) {
    let matParent = parent.matrix;
    mat = mat.premultiply(matParent);
    parent = parent.parent; 
  }
  return mat;
}
function drawSkeleton(bone) {
  let mat = getMatrix(bone);
  let bonePoint = new THREE.Vector3();
  bonePoint.setFromMatrixPosition(mat);
  
//   console.log(bone.name);
//   printMat(mat.elements);
//   console.log("");
  
  let children = bone.children;
  for(let entry of children) {
    let childBone = getMatrix(entry);
    let childPoint = new THREE.Vector3();   
    childPoint.setFromMatrixPosition(childBone);
    //console.log(bone.name, bonePoint.x, bonePoint.y, bonePoint.z);
    drawLne(bone.name, childBone.name, bonePoint, childPoint);
    drawSkeleton(entry);
  }
}


let stringToASCIICode = function(t) {
    let e = [];
    for (var n = 0; n < t.length; n++)
        e.push(t[n].charCodeAt(0));
    return e
}

function loadglb(fileName) {
    return fetch(fileName)
      .then(response => response.arrayBuffer())
};
 
function decrypt(bits, n, instance, hStr, vStr) {
  var e = Math.pow(2, 27);
  var a = e;
  e += 276;
  var o = e;
  e += 32;
  var l = e;
  e += 16;
  var c = e;
  var h = stringToASCIICode(hStr);
  var u = stringToASCIICode(vStr);
  n.set(u, l),
  n.set(h, o);
  var meth = instance["rld_setData_d"];
  meth(a, o, 256);
  var i = new Uint8Array(bits);
  n.set(i, c);
  var rld_method2 = instance["rld_method2"];
  rld_method2(a, 0, i.length, l, c, c);
  var r = c + i.length;
  var d = n[c + i.length - 1];
  if (0 !== d && d < 16) {
      n.subarray(c + i.length - d, c + i.length).slice().every((t,e,n)=>t === n[0]) && (r = c + i.length - d)
  }        
  let buffer = n.subarray(c, r).slice().buffer
  buffer = new Uint8Array(buffer)
  return buffer;
}


async function loadWebAssembly(fileName) {
  return fetch(fileName)
    .then(response => {
     return response.arrayBuffer()
    })
    .then(bits => WebAssembly.compile(bits))
    .then(module => { 
     return  WebAssembly.instantiate(module, {})
   });
 };

 let igltfexporter = new GLTFExporter();
let thisBones = [];
let  skeletonHelper = null;
 loadWebAssembly('a.wasm')
 .then(function (obj) {
 var instance = obj.exports;
 console.log('Finished compiling! Ready when you are.');
 var n = new Uint8Array(instance.memory['buffer']);

  let mixer = 0
  const clock = new THREE.Clock();
  function loop() {
    requestAnimationFrame(loop);
    const frameT = 0;//clock.getDelta();
    if(skeletonHelper != null) {
      let bones = skeletonHelper.bones;
      let bone = bones[5];

      //console.log("loop", bone.name, bone.matrixWorld.elements[0]);
    }
    

    mixer.update(frameT);
  }

  const materialRet = new THREE.MeshPhysicalMaterial( {
    clearcoat: 1.0
  } );

  let diffuseTexture = texLoader.load('./casual-f-0084.png');
  diffuseTexture.encoding = THREE.sRGBEncoding
  diffuseTexture.flipY = false;
  let bumpTexture = texLoader.load('./Character_Bump.jpg');
  bumpTexture.encoding = THREE.sRGBEncoding
  bumpTexture.flipY = false;
  let aoTexture = texLoader.load('./Character_AO.jpg');
  aoTexture.encoding = THREE.sRGBEncoding
  aoTexture.flipY = false;


 const gui = new GUI();
 function morphFun(gui, morphTargets) {
  const influences = {};
  for (const key in morphTargets) {
    const targets = morphTargets[key];
    const { child, index } = targets[0];
    influences[key] = child.morphTargetInfluences[index];
    gui.add(influences, key, 0, 1, 0.01).onChange((v) => {
      targets.forEach(({ child, index }) => {
        child.morphTargetInfluences[index] = v;
      });
    });
  }
 }

 loadglb('casual-f-0084').then(function (bits) {
     let buffer = decrypt(bits, n, instance, "ahiuQkpgjy06cLVMPn1b2vwHBqoYTOz5", "9FAKWkaLu42GCi6y");
     let decoder = new TextDecoder()
     let codeName = decoder.decode(new Uint8Array(buffer,0,4))
     const loader = new GLTFLoader();
     const dracoLoader = new DRACOLoader();
     dracoLoader.setDecoderPath( './' );
     loader.setDRACOLoader( dracoLoader );
     loader.parse(buffer.buffer, "", function ( gltf  ) {
      let cid = 'JIC71c7722421cfc14b9'
      // igltfexporter.parse(
      //   gltf.scene,
      //   function (result) { 
      //       console.log(result);
      //   },
      //   options
      // )

      const _ = gltf.scene;
      _.name = '2.gltf';
      _.updateMatrixWorld();
      // _.animations.push(...gltf.animations)
      const SkinnedMesh = gltf.scene.getObjectByName("Character");
      // console.log('骨架', SkinnedMesh.skeleton)

      for (const [key, value] of Object.entries(
        gltf.scene.children[0].children[1].morphTargetDictionary
      )) {
        //console.log('morph',  key, value)
        //gui.add(influences, value, 0, 1, 0.01).name(key).listen();
      }

      const morphTargets = {};
      gltf.scene.traverse((child) => {
        if (child.isMesh) {
          child.material.metalness = 0;
          child.material.vertexColors = false;
          child.material.map = texture;          
          if (child.morphTargetDictionary) console.log(child.morphTargetDictionary);
          if (child.morphTargetDictionary) {
            for (const key in child.morphTargetDictionary) {
              const index = child.morphTargetDictionary[key];
              if (Array.isArray(morphTargets[key])) {
                morphTargets[key].push({ index, child });
              } else {
                morphTargets[key] = [];
                morphTargets[key].push({ index, child });
              }              
            }
          }
        }
      });      
      //console.log('morph-------->', morphTargets);
      morphFun(gui, morphTargets)
      gltf.scene.traverse(function(obj) {
        if (obj.isBone) {
          //console.log('bone：', obj.name);
        }else {
          //console.log('obj', obj.name);
        }
        
        if (obj.isMesh) {
            //console.log('gltf默认材质',obj.material);
            obj.material.map = diffuseTexture;
            obj.material.alphaMap = diffuseTexture;
            obj.material.needsUpdate = true;
            obj.material.normalMap = bumpTexture;
            obj.material.needsUpdate = true;
            obj.material.aoMap = aoTexture;
            obj.material.needsUpdate = true;
            let geometry = obj.geometry;
            //console.log(geometry.attributes.position);
        }
    });

    scene.add( gltf.scene )
    //console.log(gltf.scene);
     skeletonHelper = new THREE.SkeletonHelper(gltf.scene);
    scene.add(skeletonHelper); 
 
    
    
    var grid = new THREE.GridHelper(24, 24, 0xFF0000, 0x444444);            
    grid.material.opacity = 0.4;
    grid.material.transparent = true;
    scene.add(grid);

    const bone1 = gltf.scene.getObjectByName('L_Thigh');
    gui.add(bone1.rotation, 'x', -Math.PI / 3, Math.PI / 3).name('L_Thigh');
    gui.add(bone1.rotation, 'y', -Math.PI / 3, Math.PI / 3).name('L_Thigh');
    gui.add(bone1.rotation, 'z', -Math.PI / 3, 0).name('L_Thigh');

    const V_Open = gltf.scene.getObjectByName('V_Open');
    console.log(V_Open)

    mixer = new THREE.AnimationMixer(gltf.scene);
    loadglb('idle-random').then(function (bits) {
      let buffer = decrypt(bits, n, instance, "VJhYPEHudXLni9brBFCU1awGcMpl8tjN", "d7FeTSkMjYJtxu1I")
      let decoder = new TextDecoder()
      const loader = new GLTFLoader();
      const dracoLoader = new DRACOLoader()
      dracoLoader.setDecoderPath( './' )
      loader.setDRACOLoader( dracoLoader )
      loader.parse(buffer.buffer, "", function ( gltf  ) {
        const _ = gltf.scene;
        // console.log(gltf)
        const clipAction = mixer.clipAction(gltf.animations[0]);        
        clipAction.play();
        loop(); 
        const options = {
          trs: false,     
          onlyVisible: true, 
          animations: gltf.animations,
          truncateDrawRange: true,
          binary: false,
          maxTextureSize: Infinity,
        };
      let animation = gltf.animations[0]
      let duration = animation.duration
      let animName = animation.name
      let tracks = animation.tracks

      console.log("animName:", animName, duration)
      console.log("tracks:", tracks)
      igltfexporter.parse(
          gltf.animations[0],
          function (result) { 
              console.log(result);
            //downloadFile("t123.txt", result)
          },
          options
        );           
      }, 
      function ( err ) {
          console.log("1111111111", err)
      })
      return 1
    })
    }, function ( err ) {
      console.log("1111111111", err);
  })
  return 1

 });


});
