// https://gltf-viewer.donmccurdy.com/
// https://gltf.nsdt.cloud/
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { DRACOLoader } from 'three/addons/loaders/DRACOLoader.js';
import { FBXLoader } from 'three/addons/loaders/FBXLoader'
import { GLTFExporter } from "three/addons/exporters/GLTFExporter.js";
import {GUI} from 'three/addons/libs/lil-gui.module.min.js';
import * as R from 'myLib'
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer();
const controls = new OrbitControls( camera, renderer.domElement );

renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);
 
const geometry = new THREE.BoxGeometry(1, 1, 1);
const material = new THREE.MeshBasicMaterial({ color: 0x00ff00 });


const light2 = new THREE.AmbientLight(0xffffff, 1); // soft white light
scene.add(light2);
//直线光源
const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
directionalLight.position.set(10, 10, 10);
scene.add(directionalLight);
camera.position.z = 5;
 

 let texLoader = new THREE.TextureLoader()


function animate() {
    requestAnimationFrame(animate);
    renderer.render(scene, camera);
}
animate();

const loader = new GLTFLoader();
// const dracoLoader = new DRACOLoader();
// dracoLoader.setDecoderPath( './' );
// loader.setDRACOLoader( dracoLoader );
//  -----------------------------------------------------------------------------
loader.load( './2.gltf', function ( gltf ) {
console.log('--->', gltf)
scene.add( gltf.scene );
const skeletonHelper = new THREE.SkeletonHelper(gltf.scene);
scene.add(skeletonHelper);
console.log(skeletonHelper);
let idx = 0      
gltf.scene.traverse(function(obj) {
  if (obj.isBone) {
    idx++;
    console.log('bone：', idx, obj.name);
  }else {
    //console.log('obj', obj.name);
  }
});

} );

