<template>
  <div class="scene-root">
    <!-- 左侧面板容器 -->
    <div class="panels-wrapper">
      <!-- 左侧第一列：组件列表面板 -->
      <aside class="component-panel left-panel">
        <div class="panel-title">Components</div>
        <div class="panel-count">
          Total: {{ filteredComponentList.length }} / {{ componentList.length }}
          <span v-if="selectedComponentNames.length > 0" class="selected-count">
            | Selected: {{ selectedComponentNames.length }}
          </span>
        </div>
        <div class="filter-box">
          <input
            v-model="filterText"
            type="text"
            class="filter-input"
            placeholder="Filter components..."
            @keyup.escape="clearFilter"
          />
          <button v-if="filterText" class="filter-clear" @click="clearFilter">✕</button>
        </div>

        <div v-if="selectedComponentNames.length > 0" class="action-buttons">
          <button class="delete-selection-btn" @click="deleteSelected">🗑 Delete Selected</button>
          <button class="clear-selection-btn" @click="clearSelection">✕ Clear Selection</button>
          <button class="export-btn" @click="exportJSON">📥 Export JSON</button>
          <div v-if="exportMessage" class="export-msg">{{ exportMessage }}</div>
        </div>
        <div class="component-flow">
          <div
            v-for="item in filteredComponentList"
            :key="item.name"
            class="component-chip"
            :class="{ selected: selectedComponentNames.includes(item.name), deleted: deletedComponentNames.has(item.name) }"
            @click="toggleComponentSelection(item.name, $event)"
          >
            <span class="chip-name">{{ item.name }}</span>
            <span class="chip-type">{{ item.type }}</span>
            <span v-if="item.parent" class="chip-parent">parent: {{ item.parent }}</span>
          </div>
        </div>
      </aside>

      <!-- 左侧第二列：变换控制面板 -->
      <aside class="component-panel transform-panel" >

         <!-- 新增：Rebuild 始终显示 -->
        <div class="rebuild-section">
          <button class="rebuild-btn" @click="rebuildScene" :disabled="isLoading">
            <span v-if="isLoading">⏳ Rebuilding...</span>
            <span v-else>🔄 Rebuild from Export Data</span>
          </button>
        </div>

        <!-- 选中时显示变换控件 -->
        <template v-if="selectedComponentNames.length > 0">
          <div class="panel-title">Transform</div>
          <!-- 原有的 Position、Scale、Size 控件 -->
        </template>

  

        <div class="panel-title">Transform</div>
        <div class="transform-section">
          <div class="transform-group">
            <div class="transform-group-title">Position</div>
            <div class="transform-title-info">
              <span v-if="selectedComponentNames.length === 1">
                {{ selectedComponentNames[0] }}
              </span>
              <span v-else>
                {{ selectedComponentNames.length }} components selected
              </span>
            </div>
            <div class="transform-row">
              <span class="axis-label axis-x">X</span>
              <button class="dir-btn" @click="moveSelected('-x')">-</button>
              <button class="dir-btn" @click="moveSelected('+x')">+</button>
            </div>
            <div class="transform-row">
              <span class="axis-label axis-y">Y</span>
              <button class="dir-btn" @click="moveSelected('-y')">-</button>
              <button class="dir-btn" @click="moveSelected('+y')">+</button>
            </div>
            <div class="transform-row">
              <span class="axis-label axis-z">Z</span>
              <button class="dir-btn" @click="moveSelected('-z')">-</button>
              <button class="dir-btn" @click="moveSelected('+z')">+</button>
            </div>
            <div class="transform-step">
              <label>
                Step:
                <select v-model="moveStep" class="step-select">
                  <option :value="0.01">0.01</option>
                  <option :value="0.05">0.05</option>
                  <option :value="0.1">0.1</option>
                  <option :value="0.5">0.5</option>
                  <option :value="1.0">1.0</option>
                </select>
              </label>
            </div>
          </div>

          <div class="transform-divider"></div>

          <div class="transform-group">
            <div class="transform-group-title">Scale</div>
            <div class="transform-scale-display">{{ formatScale(selectedScale) }}</div>
            <div class="transform-row">
              <span class="axis-label axis-x">X</span>
              <button class="dir-btn" @click="scaleSelected('-x')">-</button>
              <button class="dir-btn" @click="scaleSelected('+x')">+</button>
            </div>
            <div class="transform-row">
              <span class="axis-label axis-y">Y</span>
              <button class="dir-btn" @click="scaleSelected('-y')">-</button>
              <button class="dir-btn" @click="scaleSelected('+y')">+</button>
            </div>
            <div class="transform-row">
              <span class="axis-label axis-z">Z</span>
              <button class="dir-btn" @click="scaleSelected('-z')">-</button>
              <button class="dir-btn" @click="scaleSelected('+z')">+</button>
            </div>
            <div class="transform-step">
              <label>
                Step:
                <select v-model="scaleStep" class="step-select">
                  <option :value="0.01">0.01</option>
                  <option :value="0.05">0.05</option>
                  <option :value="0.1">0.1</option>
                  <option :value="0.25">0.25</option>
                  <option :value="0.5">0.5</option>
                </select>
              </label>
            </div>
          </div>

          <div class="transform-divider"></div>
          <!-- 颜色设置面板 -->
          <div class="transform-group">
            <div class="transform-group-title">Color</div>
            <div class="transform-title-info">
              <span v-if="selectedComponentNames.length === 1">
                {{ selectedComponentNames[0] }}
              </span>
              <span v-else-if="selectedComponentNames.length > 1">
                {{ selectedComponentNames.length }} components
              </span>
              <span v-else>
                No selection
              </span>
            </div>
            
            <!-- 颜色选择器 -->
            <div v-if="selectedComponentNames.length > 0" class="color-picker-section">
              <div class="color-preview-row">
                <label class="color-input-label" title="Click to pick color">
                  <div 
                    class="color-preview" 
                    :style="{ backgroundColor: `rgb(${currentColor.map(c => Math.round(c * 255)).join(',')})` }"
                  ></div>
                  <input 
                    type="color" 
                    :value="rgbToHex(currentColor)"
                    @input="onColorPickerChange"
                    class="color-picker-input"
                  />
                </label>
                <span class="color-hex">{{ rgbToHex(currentColor) }}</span>
              </div>
              
              <!-- RGB 数值显示 -->
              <div class="color-rgb-values">
                <span>R: {{ Math.round(currentColor[0] * 255) }}</span>
                <span>G: {{ Math.round(currentColor[1] * 255) }}</span>
                <span>B: {{ Math.round(currentColor[2] * 255) }}</span>
              </div>
              
              <!-- 快速预设颜色 -->
              <div class="preset-colors">
                <div 
                  v-for="preset in colorPresets" 
                  :key="preset.name"
                  class="preset-color-dot"
                  :style="{ backgroundColor: `rgb(${preset.color.map(c => Math.round(c * 255)).join(',')})` }"
                  :title="preset.name"
                  @click="applyPresetColor(preset.color)"
                ></div>
              </div>
              
              <!-- 重置颜色按钮 -->
              <button class="reset-color-btn" @click="resetColor">↺ Reset Original Color</button>
            </div>
            
            <!-- 未选中时的提示 -->
            <div v-else class="no-selection-hint">
              Select component(s) to edit color
            </div>
          </div>
        </div>
      </aside>
    </div>

    <div ref="container" class="canvas-container"></div>
  </div>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import * as THREE from 'three'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls'
import { SUBTRACTION, Brush, Evaluator } from 'three-bvh-csg'

const container = ref<HTMLElement | null>(null)
let renderer: THREE.WebGLRenderer | null = null
let scene: THREE.Scene | null = null
let camera: THREE.PerspectiveCamera | null = null
let controls: OrbitControls | null = null
let animationId = 0

// 原始 JSON 缓存（从文件加载后不再修改，用于导出和参考）
let cachedJSON: { objects: any[] } | null = null
// 运行时定义（用于渲染，位置会随移动更新）
const objectDefinitions: Record<string, any> = {}
// 记录被移动过的对象
const movedObjects = new Set<string>()
// 记录被删除的对象名称
const deletedComponentNames = ref(new Set<string>())
const HIDE_WINDOW_MESHES = false
const componentList = ref<Array<{ name: string; type: string; parent?: string }>>([])
const filterText = ref('')
const selectedComponentNames = ref<string[]>([])
const moveStep = ref(0.1)
const scaleStep = ref(0.1)
const selectedScale = ref<[number, number, number]>([1, 1, 1])
const exportMessage = ref('')
const meshByComponentName: Record<string, THREE.Object3D> = {}
const originalSizes: Record<string, [number, number, number] | [number]> = {}
const selectionBoxHelpers: Record<string, THREE.BoxHelper> = {}
const isLoading = ref(false)

// ============ 伸缩手柄相关 ============
let scaleHandle: THREE.Object3D | null = null          // 当前显示的伸缩手柄
const handleStep = 0.01                               // 伸缩步长

// ★ 新增：拖拽状态变量
let isDraggingHandle = false
let dragPlane = new THREE.Plane()                     // 垂直于相机视线或法线的拖拽平面
let dragStartPoint = new THREE.Vector3()              // 拖拽起点（世界坐标）
let dragNormal = new THREE.Vector3()                  // 拖拽方向（面法线）
let dragOffset = new THREE.Vector3()                  // 手柄初始位置到拖拽起点的偏移
let handleTargetName = ''                             // 手柄对应的物体名称
let lastMousePosition = new THREE.Vector2()           // 上一帧鼠标位置（用于计算移动量）

// ============ 颜色相关 ============

// 当前选中组件的颜色
const currentColor = ref<number[]>([1, 1, 1])
// 存储每个组件原始颜色的备份
const originalColors = new Map<string, number[]>()
// 记录颜色被修改过的对象
const colorModifiedObjects = new Set<string>()

// 预设颜色列表
const colorPresets = [
  { name: 'Red', color: [0.9, 0.1, 0.1] },
  { name: 'Orange', color: [0.98, 0.6, 0.1] },
  { name: 'Yellow', color: [0.95, 0.95, 0.1] },
  { name: 'Green', color: [0.1, 0.8, 0.3] },
  { name: 'Cyan', color: [0.1, 0.9, 0.9] },
  { name: 'Blue', color: [0.1, 0.3, 0.9] },
  { name: 'Purple', color: [0.6, 0.2, 0.8] },
  { name: 'Pink', color: [0.95, 0.4, 0.6] },
  { name: 'White', color: [0.95, 0.95, 0.95] },
  { name: 'Gray', color: [0.5, 0.5, 0.5] },
  { name: 'Dark', color: [0.15, 0.15, 0.15] },
  { name: 'Gold', color: [0.95, 0.8, 0.2] },
]

/**
 * 将 RGB 数组（0-1 范围）转换为 CSS Hex 字符串
 */
const rgbToHex = (color: number[]): string => {
  if (!color || color.length < 3) return '#ffffff'
  const r = Math.max(0, Math.min(255, Math.round(color[0] * 255)))
  const g = Math.max(0, Math.min(255, Math.round(color[1] * 255)))
  const b = Math.max(0, Math.min(255, Math.round(color[2] * 255)))
  return `#${((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1)}`
}

/**
 * 将 CSS Hex 字符串转换为 RGB 数组（0-1 范围）
 */
const hexToRgb = (hex: string): number[] => {
  const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex)
  if (!result) return [1, 1, 1]
  return [
    Math.max(0, Math.min(1, parseInt(result[1], 16) / 255)),
    Math.max(0, Math.min(1, parseInt(result[2], 16) / 255)),
    Math.max(0, Math.min(1, parseInt(result[3], 16) / 255)),
  ]
}

/**
 * 颜色选择器值改变时
 */
const onColorPickerChange = (event: Event) => {
  const target = event.target as HTMLInputElement
  const hex = target.value
  const rgb = hexToRgb(hex)
  currentColor.value = rgb
  applyColorToSelected(rgb)
}

/**
 * 应用颜色到所有选中的组件
 */
const applyColorToSelected = (color: number[]) => {
  if (selectedComponentNames.value.length === 0) return
  
  selectedComponentNames.value.forEach(name => {
    const def = objectDefinitions[name]
    if (!def) return
    
    // 保存原始颜色（如果尚未保存）
    if (def.color && !originalColors.has(name)) {
      originalColors.set(name, [...def.color])
    }
    
    // 更新 objectDefinitions 中的颜色
    def.color = [...color]
    
    // 标记颜色被修改
    colorModifiedObjects.add(name)
  })
  
  // 重建场景以更新 CSG 对象的颜色
  rebuildScene()
}

/**
 * 递归更新 mesh 或其所有子 mesh 的颜色
 */
const updateMeshColor = (obj: THREE.Object3D, color: number[]) => {
  obj.traverse(child => {
    if (child instanceof THREE.Mesh) {
      const materials = Array.isArray(child.material) ? child.material : [child.material]
      materials.forEach(mat => {
        if (mat && 'color' in mat && mat.color instanceof THREE.Color) {
          mat.color.setRGB(color[0], color[1], color[2])
        }
      })
    }
  })
}

/**
 * 应用预设颜色
 */
const applyPresetColor = (color: number[]) => {
  currentColor.value = [...color]
  applyColorToSelected(color)
}

/**
 * 重置为原始颜色
 */
const resetColor = () => {
  if (selectedComponentNames.value.length === 0) return
  
  selectedComponentNames.value.forEach(name => {
    const def = objectDefinitions[name]
    if (!def) return
    
    const originalColor = originalColors.get(name)
    if (originalColor) {
      def.color = [...originalColor]
      colorModifiedObjects.delete(name)
      originalColors.delete(name)
    }
  })
  
  // 更新显示为第一个选中组件的颜色
  if (selectedComponentNames.value.length > 0) {
    const firstDef = objectDefinitions[selectedComponentNames.value[0]]
    if (firstDef && firstDef.color) {
      currentColor.value = [...firstDef.color]
    }
  }
  
  rebuildScene()
}

/**
 * 更新当前颜色显示（选中组件改变时调用）
 */
const updateCurrentColorDisplay = () => {
  if (selectedComponentNames.value.length === 0) {
    currentColor.value = [1, 1, 1]
    return
  }
  
  const firstSelected = selectedComponentNames.value[0]
  const def = objectDefinitions[firstSelected]
  if (def && def.color) {
    currentColor.value = [...def.color]
  } else {
    currentColor.value = [1, 1, 1]
  }
}

// 双击选择相关变量
const raycaster = new THREE.Raycaster()
const mouse = new THREE.Vector2()
let lastClickTime = 0
let lastClickObject: THREE.Object3D | null = null

const filteredComponentList = computed(() => {
  const query = filterText.value.trim().toLowerCase()
  let list = componentList.value
  
  // 过滤掉已删除的组件
  list = list.filter(item => !deletedComponentNames.value.has(item.name))
  
  if (!query) return list
  return list.filter(item => item.name.toLowerCase().includes(query))
})

const clearFilter = () => {
  filterText.value = ''
}

const formatScale = (scale: [number, number, number]) => {
  return `${scale[0].toFixed(2)}, ${scale[1].toFixed(2)}, ${scale[2].toFixed(2)}`
}

let exportTimeout: ReturnType<typeof setTimeout> | null = null

const getMeshWorldPosition = (obj: THREE.Object3D): THREE.Vector3 => {
  const worldPos = new THREE.Vector3()
  obj.getWorldPosition(worldPos)
  return worldPos
}

const getParentWorldPosition = (parentName: string): THREE.Vector3 | null => {
  const parentMesh = meshByComponentName[parentName]
  if (parentMesh) {
    return getMeshWorldPosition(parentMesh)
  }

  const parentDef = objectDefinitions[parentName]
  if (parentDef) {
    const worldMatrix = getWorldMatrix(parentDef)
    const pos = new THREE.Vector3()
    pos.setFromMatrixPosition(worldMatrix)
    return pos
  }

  return null
}

const getWorldMatrix = (obj: any, visited = new Set<string>()): THREE.Matrix4 => {
  const local = getLocalMatrix(obj)
  if (!obj.parent) return local

  const parentName = String(obj.parent)
  if (visited.has(parentName)) {
    return local
  }

  const parentObj = objectDefinitions[parentName]
  if (!parentObj) return local

  visited.add(parentName)
  const parentWorld = getWorldMatrix(parentObj, visited)
  return parentWorld.multiply(local)
}

const getRelativePosition = (def: any): [number, number, number] | null => {
  if (!def.position) return null

  if (!def.parent) {
    return [...def.position]
  }

  const parentDef = objectDefinitions[def.parent]
  if (!parentDef || !parentDef.position) {
    return [...def.position]
  }

  return [
    def.position[0] - parentDef.position[0],
    def.position[1] - parentDef.position[1],
    def.position[2] - parentDef.position[2],
  ]
}

// 获取导出数据（包含所有运行时修改，排除已删除的对象）
const getExportData = () => {
  if (!cachedJSON) {
    return null
  }

  const exportedObjects = cachedJSON.objects
    .filter((cachedObj: any) => {
      // 过滤掉已删除的对象
      return !deletedComponentNames.value.has(cachedObj.name)
    })
    .map((cachedObj: any) => {
      const name = cachedObj.name
      const runtimeDef = name ? objectDefinitions[name] : null
      const exported: any = {}
      // 复制所有原始属性
      for (const key of Object.keys(cachedObj)) {
        exported[key] = cachedObj[key]
      }
      // 覆盖运行时修改过的属性
      if (runtimeDef) {
        // 只对移动过的对象使用叠加
        if (name && movedObjects.has(name) && cachedObj.position) {
          const meshObj = meshByComponentName[name]
          if (meshObj) {
            // exported.position = [
            //   cachedObj.position[0],
            //   cachedObj.position[1],
            //   cachedObj.position[2]
            // ]
          } else {
            // subtract 对象，直接使用运行时定义的位置（相对坐标）
            exported.position = [...runtimeDef.position]
          }
        }
        // if (runtimeDef.size) {
        //   exported.size = [...runtimeDef.size]
        // }
        if (cachedObj.type === 'cylinder') {
          if (runtimeDef.radius !== undefined) exported.radius = runtimeDef.radius
          if (runtimeDef.height !== undefined) exported.height = runtimeDef.height
        }
        
        // 颜色
        if (colorModifiedObjects.has(name) && runtimeDef.color) {
          exported.color = [...runtimeDef.color]
        }
      }
      return exported
    })

  return { objects: exportedObjects }
}

const exportJSON = () => {
  const exportData = getExportData()
  
  if (!exportData) {
    exportMessage.value = '❌ No cached JSON'
    if (exportTimeout) clearTimeout(exportTimeout)
    exportTimeout = setTimeout(() => { exportMessage.value = '' }, 3000)
    return
  }

  const jsonStr = JSON.stringify(exportData, null, 2)
  navigator.clipboard.writeText(jsonStr).then(() => {
    exportMessage.value = '✅ Copied to clipboard!'
  }).catch(() => {
    const blob = new Blob([jsonStr], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'bus_modified.json'
    a.click()
    URL.revokeObjectURL(url)
    exportMessage.value = '⬇ Downloaded bus_modified.json'
  })
  if (exportTimeout) clearTimeout(exportTimeout)
  exportTimeout = setTimeout(() => {
    exportMessage.value = ''
  }, 3000)
}

const updateScaleDisplay = () => {
  if (selectedComponentNames.value.length === 0) {
    selectedScale.value = [1, 1, 1]
    return
  }
  const firstSelected = selectedComponentNames.value[0]
  const mesh = meshByComponentName[firstSelected]
  if (mesh) {
    selectedScale.value = [mesh.scale.x, mesh.scale.y, mesh.scale.z]
  }
}

const setMeshHighlighted = (name: string, highlighted: boolean) => {
  const mesh= meshByComponentName[name] as THREE.Object3D
  if (!mesh) return
  mesh.traverse(child => {
    if (child instanceof THREE.Mesh) {
      const materials = Array.isArray(child.material) ? child.material : [child.material]
      materials.forEach(material => {
        if (!(material instanceof THREE.MeshStandardMaterial || material instanceof THREE.MeshPhysicalMaterial)) {
          return
        }
        if (highlighted) {
          if (material.userData.__origEmissive === undefined) {
            material.userData.__origEmissive = material.emissive.getHex()
            material.userData.__origEmissiveIntensity = material.emissiveIntensity
          }
          material.emissive.setHex(0x22c55e)
          material.emissiveIntensity = 0.9
		  addBoundingBox(name)
        } else if (material.userData.__origEmissive !== undefined) {
          material.emissive.setHex(material.userData.__origEmissive)
          material.emissiveIntensity = material.userData.__origEmissiveIntensity ?? 1
		  removeBoundingBox(name)
        }
      })
    }
  })
}

const addBoundingBox = (name: string) => {
  if (selectionBoxHelpers[name]) return
  
  const def = objectDefinitions[name]
  if (!def) return
  
  // 从 objectDefinitions 获取当前定义（包含运行时修改）
  const currentDef = objectDefinitions[name]
  if (!currentDef) return
  
  // 创建临时几何体
  let geometry: THREE.BufferGeometry
  
  if (currentDef.type === 'box' || currentDef.shape === 'box' || currentDef.type === 'subtract') {
    const size = currentDef.size || [1, 1, 1]
    geometry = new THREE.BoxGeometry(size[0], size[1], size[2])
  } else if (currentDef.type === 'cylinder' || currentDef.shape === 'cylinder') {
    geometry = new THREE.CylinderGeometry(
      currentDef.radius || 0.5, 
      currentDef.radius || 0.5, 
      currentDef.height || 1, 
      16
    )
  } else {
    return
  }
  
  const tempMesh = new THREE.Mesh(geometry)
  
  // 计算当前位置
  let worldPos = new THREE.Vector3(
    currentDef.position?.[0] || 0,
    currentDef.position?.[1] || 0,
    currentDef.position?.[2] || 0
  )
  
  // 如果是 subtract 对象或子对象，需要加上父对象的位置
  if ((currentDef.type === 'subtract' || currentDef.shape) && currentDef.parent) {
    const parentDef = objectDefinitions[currentDef.parent]
    if (parentDef && parentDef.position) {
      worldPos.x += parentDef.position[0]
      worldPos.y += parentDef.position[1]
      worldPos.z += parentDef.position[2]
    }
  }
  
  // 如果对象有 mesh 且被移动过，加上偏移量
  if (movedObjects.has(name)) {
    const mesh = meshByComponentName[name]
    if (mesh) {
      worldPos.x += mesh.position.x
      worldPos.y += mesh.position.y
      worldPos.z += mesh.position.z
    }
  }
  
  tempMesh.position.copy(worldPos)
  
  // 应用旋转
  if (currentDef.rotation) {
    tempMesh.rotation.set(
      (currentDef.rotation[0] * Math.PI) / 180,
      (currentDef.rotation[1] * Math.PI) / 180,
      (currentDef.rotation[2] * Math.PI) / 180
    )
  }
  
  const boxHelper = new THREE.BoxHelper(tempMesh, 0x22c55e)
  scene?.add(boxHelper)
  selectionBoxHelpers[name] = boxHelper
}

const removeBoundingBox = (name: string) => {
  const boxHelper = selectionBoxHelpers[name]
  if (boxHelper) {
    scene?.remove(boxHelper)
    delete selectionBoxHelpers[name]
  }
}

const clearSelection = () => {
  selectedComponentNames.value.forEach(name => {
    setMeshHighlighted(name, false)    
  })
  selectedComponentNames.value = []
  updateScaleDisplay()
  updateCurrentColorDisplay()
  hideScaleHandle() // 清除选择时隐藏手柄
}

const toggleComponentSelection = (name: string, event?: MouseEvent) => {
  const isCtrlPressed = event?.ctrlKey || event?.metaKey
  
  if (isCtrlPressed) {
    const index = selectedComponentNames.value.indexOf(name)
    if (index === -1) {
      selectedComponentNames.value.push(name)
      setMeshHighlighted(name, true)      
    } else {
      selectedComponentNames.value.splice(index, 1)
      setMeshHighlighted(name, false)
    }
    updateScaleDisplay()
    updateCurrentColorDisplay()
  } else {
    selectedComponentNames.value.forEach(selectedName => {
      setMeshHighlighted(selectedName, false)
    })
    
    if (selectedComponentNames.value.length === 1 && selectedComponentNames.value[0] === name) {
      selectedComponentNames.value = []
    } else {
      selectedComponentNames.value = [name]
      setMeshHighlighted(name, true)
    }
    updateScaleDisplay()
    updateCurrentColorDisplay()
  }
}

const moveSelected = (direction: string) => {
  if (selectedComponentNames.value.length === 0) return
    const step = moveStep.value
    selectedComponentNames.value.forEach(name => {
    const mesh = meshByComponentName[name]
    //const def = objectDefinitions[name]
    if (mesh) {
      // 有 mesh 的对象，直接移动
      switch (direction) {
        case '+x': mesh.position.x += step; break
        case '-x': mesh.position.x -= step; break
        case '+y': mesh.position.y += step; break
        case '-y': mesh.position.y -= step; break
        case '+z': mesh.position.z += step; break
        case '-z': mesh.position.z -= step; break
      }
      let cachedObj = cachedJSON?.objects.find((obj: any) => obj.name === name)
      if (cachedObj) {
        cachedObj.position = [mesh.position.x, mesh.position.y, mesh.position.z]
      }
    }
    //else if (def && (def.type === 'subtract' || def.shape)) {
      // subtract 对象，更新相对父对象的局部坐标
      // switch (direction) {
      //   case '+x': def.position[0] += step; break
      //   case '-x': def.position[0] -= step; break
      //   case '+y': def.position[1] += step; break
      //   case '-y': def.position[1] -= step; break
      //   case '+z': def.position[2] += step; break
      //   case '-z': def.position[2] -= step; break
      // }
    //}
    // 标记为已移动
    movedObjects.add(name)

  })
  
  // 更新包围盒
  selectedComponentNames.value.forEach(name => {
    const boxHelper = selectionBoxHelpers[name]
    if (boxHelper) {
      boxHelper.update()
    }
  })

  rebuildScene()
  
}

const scaleSelected = (direction: string) => {
  if (selectedComponentNames.value.length === 0) return
  
  const step = scaleStep.value
  const sign = direction.startsWith('+') ? 1 : -1
  const axis = direction.slice(1) as 'x' | 'y' | 'z'
  
  selectedComponentNames.value.forEach(name => {
    const mesh = meshByComponentName[name] as THREE.Mesh
     let cachedObj = cachedJSON?.objects.find((obj: any) => obj.name === name)
    if (!mesh) return
    const oldScale = mesh.scale[axis]
    const newVal = THREE.MathUtils.clamp(mesh.scale[axis] + sign * step, 0.01, 100)
    const deltaScale = newVal - oldScale
    mesh.scale[axis] = newVal
    if(!mesh.geometry.boundingBox) {
      mesh.geometry.computeBoundingBox()
    }
    const bbox = mesh.geometry.boundingBox!
    const rawLength = bbox.max[axis] - bbox.min[axis]
    const localDir = new THREE.Vector3()
    if (axis === 'x') {
      localDir.set(1, 0, 0)
    }
    else if (axis === 'y') {
        localDir.set(0, 1, 0) 
    }
    else {
      localDir.set(0, 0, 1)
    }
    localDir.applyQuaternion(mesh.quaternion)
    const moveDistance = rawLength * deltaScale / 2
    mesh.position.addScaledVector(localDir, moveDistance)
    cachedObj.position = [mesh.position.x, mesh.position.y, mesh.position.z]
    console.log("moveDistance:", moveDistance)
      
    const def = objectDefinitions[name]
    if (def) {
      if (def.type === 'cylinder' && def.radius !== undefined) {
        const origRadius = originalSizes[name]?.[0] ?? def.radius
        if (axis === 'x' || axis === 'y') {
          def.radius = origRadius * newVal
        }
        if (def.height !== undefined && axis === 'z') {
          const origHeight = (originalSizes[name] as [number])?.[1] ?? def.height
          def.height = origHeight * newVal
        }
      } else if (def.size) {
        const origSize = (originalSizes[name] as [number, number, number]) ?? [...def.size]
        const idx = axis === 'x' ? 0 : axis === 'y' ? 1 : 2
        def.size[idx] = origSize[idx] * newVal
       
        if (cachedObj) {
          cachedObj.size[idx] = origSize[idx] * newVal
        }
      }
    }
    
    // 更新包围盒
    const boxHelper = selectionBoxHelpers[name]
    if (boxHelper) {
      boxHelper.update()
    }
  })
  
  updateScaleDisplay()

  rebuildScene()
}

// 删除选中的组件
const deleteSelected = () => {
  if (selectedComponentNames.value.length === 0) return
  
  // 收集所有要删除的名称（包括子对象）
  const namesToDelete = new Set<string>()
  
  selectedComponentNames.value.forEach(name => {
    namesToDelete.add(name)
    
    // 如果删除的是父对象，也删除其所有 subtract 子对象
    if (cachedJSON) {
      cachedJSON.objects.forEach((obj: any) => {
        if (obj.type === 'subtract' && obj.parent === name) {
          if (obj.name) {
            namesToDelete.add(obj.name)
          }
        }
      })
    }
  })
  
  // 添加到删除集合
  namesToDelete.forEach(name => {
    deletedComponentNames.value.add(name)
  })
  
  // 清除选择
  clearSelection()
  
  // 重建场景
  rebuildScene()
}

const isGlassObjectName = (name?: string) => {
  if (!name) return false
  return /(side_window|glass|windshield)/i.test(name) && !/^seat_/i.test(name)
}

const keyState: Record<'KeyW' | 'KeyA' | 'KeyS' | 'KeyD' | 'ArrowUp' | 'ArrowDown', boolean> = {
  KeyW: false,
  KeyA: false,
  KeyS: false,
  KeyD: false,
  ArrowUp: false,
  ArrowDown: false,
}

const onKeyDown = (event: KeyboardEvent) => {
  if (event.code in keyState) {
    keyState[event.code as keyof typeof keyState] = true
  }
  
  // 处理 Delete 键
  if (event.code === 'Delete' || event.code === 'Backspace') {
    // 防止在输入框中按删除键时触发
    const target = event.target as HTMLElement
    if (target.tagName === 'INPUT' || target.tagName === 'TEXTAREA' || target.isContentEditable) {
      return
    }
    
    if (selectedComponentNames.value.length > 0) {
      event.preventDefault()
      deleteSelected()
    }
  }
}

const onKeyUp = (event: KeyboardEvent) => {
  if (event.code in keyState) {
    keyState[event.code as keyof typeof keyState] = false
  }
}

// ============ 伸缩手柄相关函数 ============

/**
 * 显示伸缩手柄
 * @param targetMesh - 被双击的 mesh
 * @param faceNormal - 面的世界法向量
 * @param point     - 点击点的世界坐标
 */
const showScaleHandle = (targetMesh: THREE.Object3D, faceNormal: THREE.Vector3, point: THREE.Vector3) => {
  // 移除已有手柄
  hideScaleHandle()

  if (!scene) return

  const handleGroup = new THREE.Group()
  const handleGeom = new THREE.CylinderGeometry(0.05, 0.05, 0.5, 8)
  const handleMat = new THREE.MeshBasicMaterial({ color: 0xff4444 })
  const handleMesh = new THREE.Mesh(handleGeom, handleMat)

  // ★ 标记为手柄，便于射线检测识别
  handleMesh.userData.isScaleHandle = true

  // 默认圆柱体沿 Y 轴，旋转至法向量方向
  const quat = new THREE.Quaternion().setFromUnitVectors(
    new THREE.Vector3(0, 1, 0),
    faceNormal.clone().normalize()
  )
  handleMesh.setRotationFromQuaternion(quat)

  // 稍微沿法线方向偏移，避免与物体表面重叠
  const offset = faceNormal.clone().normalize().multiplyScalar(0.25)
  handleMesh.position.copy(point.clone().add(offset))

  handleGroup.add(handleMesh)
  scene.add(handleGroup)
  scaleHandle = handleGroup

  // 保存法线方向，供拖拽使用
  dragNormal.copy(faceNormal.clone().normalize())
}

/**
 * 隐藏伸缩手柄
 */
const hideScaleHandle = () => {
  // 如果正在拖拽，先结束拖拽（endHandleDrag 会负责移除手柄）
  if (isDraggingHandle) {
    endHandleDrag()
    return
  }
  // 否则直接移除手柄
  if (scaleHandle && scene) {
    scene.remove(scaleHandle)
    scaleHandle = null
  }
}

/**
 * 开始拖拽手柄
 */
const startHandleDrag = (point: THREE.Vector3) => {
  if (!scaleHandle || !camera) return

  // 禁用轨道控制
  if (controls) controls.enabled = false

  isDraggingHandle = true
  dragStartPoint.copy(point)

  // 记录手柄当前世界位置（用于计算偏移）
  const handleWorldPos = new THREE.Vector3()
  scaleHandle.getWorldPosition(handleWorldPos)
  dragOffset.subVectors(handleWorldPos, point)

  // 构建拖拽平面：过 point，法向量朝向相机（方便屏幕映射）
  const cameraDir = new THREE.Vector3()
  camera.getWorldDirection(cameraDir)
  dragPlane.setFromNormalAndCoplanarPoint(cameraDir.clone().normalize(), point)

  // 阻止浏览器默认行为（如拖拽图片等）
  if (container.value) {
    container.value.style.cursor = 'ns-resize'
  }
}

/**
 * 更新拖拽手柄位置
 */
const updateHandleDrag = (event: MouseEvent) => {
  if (!isDraggingHandle || !scaleHandle || !camera || !container.value) return

  const rect = container.value.getBoundingClientRect()
  const mouse = new THREE.Vector2(
    ((event.clientX - rect.left) / rect.width) * 2 - 1,
    -((event.clientY - rect.top) / rect.height) * 2 + 1
  )

  const raycaster = new THREE.Raycaster()
  raycaster.setFromCamera(mouse, camera)

  const targetPoint = new THREE.Vector3()
  const intersect = raycaster.ray.intersectPlane(dragPlane, targetPoint)

  if (intersect) {
    // 计算沿法线方向的位移量
    const movement = targetPoint.clone().sub(dragStartPoint)
    const delta = movement.dot(dragNormal) // 投影到法线方向

    // 更新手柄位置
    scaleHandle.position.copy(dragStartPoint.clone().add(dragNormal.clone().multiplyScalar(delta)).add(dragOffset))
  }
}

/**
 * 结束拖拽手柄，应用伸缩并重建场景
 */
const endHandleDrag = () => {
  if (!isDraggingHandle) return

  // 重新启用轨道控制
  if (controls) controls.enabled = true

  // 计算最终伸缩量
  let totalDelta = 0
  if (scaleHandle && camera) {
    const currentPos = new THREE.Vector3()
    scaleHandle.getWorldPosition(currentPos)
    totalDelta = currentPos.clone().sub(dragStartPoint).dot(dragNormal)
  }

  // 在重建场景前清理拖拽状态和手柄，防止循环调用
  if (scaleHandle && scene) {
    scene.remove(scaleHandle)
    scaleHandle = null
  }
  isDraggingHandle = false
  handleTargetName = ''
  if (container.value) {
    container.value.style.cursor = ''
  }

  // 应用伸缩（若有明显位移）
  if (Math.abs(totalDelta) > 0.001) {
    stretchFace(totalDelta, dragNormal)
    rebuildScene()
  }
}

// ★ 修改 stretchFace 实现，用于根据 delta 修改物体尺寸
/**
 * 伸缩选定面的函数
 * @param delta 正值拉伸，负值收缩（沿法线方向）
 * @param normal 面的法向量方向（世界空间）
 */
const stretchFace = (delta: number, normal: THREE.Vector3) => {
  if (!handleTargetName) return
  
  const def = objectDefinitions[handleTargetName]
  if (!def || def.type !== 'box') return

  // 简单实现：找到 box 最匹配法线的轴，沿该轴缩放
  // 做法：将法线转换到物体局部坐标，找到绝对值最大的分量，视为伸缩轴
  const mesh = meshByComponentName[handleTargetName]
  if (!mesh) return

  const localNormal = normal.clone().applyQuaternion(mesh.quaternion.clone().invert())
  const absX = Math.abs(localNormal.x)
  const absY = Math.abs(localNormal.y)
  const absZ = Math.abs(localNormal.z)

  let axisIndex = 0 // 0:x, 1:y, 2:z
  let sign = 1
  if (absX >= absY && absX >= absZ) {
    axisIndex = 0
    sign = localNormal.x > 0 ? 1 : -1
  } else if (absY >= absX && absY >= absZ) {
    axisIndex = 1
    sign = localNormal.y > 0 ? 1 : -1
  } else {
    axisIndex = 2
    sign = localNormal.z > 0 ? 1 : -1
  }

  const origSize = (originalSizes[handleTargetName] as [number, number, number]) || def.size
  if (!origSize) return

  const newSize = [...origSize] as [number, number, number]
  newSize[axisIndex] = Math.max(0.01, origSize[axisIndex] + sign * delta)
  
  // 更新定义中的尺寸
  def.size = newSize

  // 同时更新 cachedJSON（如果存在）
  if (cachedJSON) {
    const cachedObj = cachedJSON.objects.find((obj: any) => obj.name === handleTargetName)
    if (cachedObj) {
      cachedObj.size = [...newSize]
    }
  }

  console.log(`Stretch axis: ${axisIndex}, delta: ${delta}, new size:`, newSize)
}

// ★ 新增：mousemove 与 mouseup 全局事件处理
const onMouseMove = (event: MouseEvent) => {
  if (isDraggingHandle) {
    updateHandleDrag(event)
  }
}

const onMouseUp = (event: MouseEvent) => {
  if (isDraggingHandle) {
    endHandleDrag()
  }
}

// Shift+双击选择场景中的物体并显示伸缩手柄
const onMouseDown = (event: MouseEvent) => {
  if (!container.value || !camera) return
  
  // 如果正在拖拽手柄，直接返回（避免冲突）
  if (isDraggingHandle) {
    event.preventDefault()
    event.stopPropagation()
    return
  }

  // 计算鼠标位置
  const rect = container.value.getBoundingClientRect()
  mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1
  mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1
  
  // 从相机发射射线
  raycaster.setFromCamera(mouse, camera)
  
  // 获取所有可选择的物体
  const selectableObjects: THREE.Object3D[] = []
  Object.values(meshByComponentName).forEach(obj => {
    selectableObjects.push(obj)
  })
  // 如果存在手柄，也加入检测
  if (scaleHandle) {
    selectableObjects.push(scaleHandle)
  }
  
  // 检测射线与物体的交点
  const intersects = raycaster.intersectObjects(selectableObjects, true)
  
  // ★ 优先检查是否点击到手柄
  for (const intersect of intersects) {
    let obj = intersect.object
    while (obj) {
      if (obj.userData && obj.userData.isScaleHandle) {
        // 点击手柄，开始拖拽
        event.preventDefault()
        event.stopPropagation()
        startHandleDrag(intersect.point)
        // 记录对应的物体名称（可以通过全局变量或从当前选中的组件推断，这里假定为最近一次 Shift+双击选中的 box）
        // 为了简化，我们可以在显示手柄时把 handleTargetName 记录下来
        if (selectedComponentNames.value.length > 0) {
          handleTargetName = selectedComponentNames.value[0]
          console.log("Handle target set to:", handleTargetName)
        }
        return
      }
      obj = obj.parent as THREE.Object3D
    }
  }

  // 以下为原有的物体选择逻辑（未修改）
  // 用于记录本次点击的面法线和世界坐标
  let clickedFaceNormal: THREE.Vector3 | null = null
  let clickedPoint: THREE.Vector3 | null = null
  
  if (intersects.length > 0) {
    // 找到被点击的最顶层对象
    let clickedObject: THREE.Object3D | null = null
    
    for (const intersect of intersects) {
      let obj = intersect.object
      // 向上查找有名字的对象
      while (obj) {
        if (obj.name && meshByComponentName[obj.name]) {
          clickedObject = obj
          break
        }
        obj = obj.parent as THREE.Object3D
      }
      if (clickedObject) break
    }
    
    // 记录面的法线和交点
    if (clickedObject) {
      const firstIntersect = intersects.find(
        (i) => i.object === clickedObject || i.object.parent === clickedObject
      )
      if (firstIntersect && firstIntersect.face) {
        const normalMatrix = new THREE.Matrix3().getNormalMatrix(
          firstIntersect.object.matrixWorld
        )
        clickedFaceNormal = firstIntersect.face.normal
          .clone()
          .applyMatrix3(normalMatrix)
          .normalize()
        clickedPoint = firstIntersect.point.clone()
      }
    }
  
    if (clickedObject && clickedObject.name) {
      const currentTime = Date.now()
      const isShiftPressed = event.shiftKey // 检查 Shift 键
      
      if (isShiftPressed && currentTime - lastClickTime < 300 && lastClickObject === clickedObject) {
        // Shift+双击事件 —— 显示伸缩手柄（仅对 box 类型）
        const clickedName = clickedObject.name
        // ★ 记录当前选中物体名称，用于后续伸缩
        if (selectedComponentNames.value.length > 0) {
          handleTargetName = selectedComponentNames.value[0]
        } else {
          handleTargetName = clickedName
        }
        // 显示伸缩手柄
        const def = objectDefinitions[clickedObject.name]
        if (def && def.type === 'box' && clickedFaceNormal && clickedPoint) {
          showScaleHandle(clickedObject, clickedFaceNormal, clickedPoint)
        } else {
          hideScaleHandle()
        }
        
        lastClickTime = 0
        lastClickObject = null
      } else if (currentTime - lastClickTime < 300 && lastClickObject === clickedObject) {
        // 双击事件
        const syntheticEvent = new MouseEvent('dblclick', {
          ctrlKey: event.ctrlKey || event.metaKey,
          metaKey: event.metaKey
        })
        
        const clickedName = clickedObject.name
        
        // 找到基础对象名称和相关对象
        let baseName = clickedName
        const relatedNames: string[] = []
        
        // 如果点击的是 _cut 对象，找到基础对象名称
        if (clickedName.endsWith('_cut')) {
          baseName = clickedName.replace(/_cut$/, '')
          relatedNames.push(baseName) // 添加基础对象
          relatedNames.push(clickedName) // 添加当前 _cut 对象
          
          // 查找同名的所有 _cut 变体（如 _arch, 普通 _cut 等）
          if (cachedJSON) {
            cachedJSON.objects.forEach((obj: any) => {
              if (obj.type === 'subtract' && obj.parent === baseName) {
                if (obj.name && !relatedNames.includes(obj.name)) {
                  relatedNames.push(obj.name)
                }
              }
            })
          }
        } else {
          // 点击的是基础对象
          relatedNames.push(clickedName) // 添加基础对象
          
          // 查找所有关联的 subtract 对象
          if (cachedJSON) {
            cachedJSON.objects.forEach((obj: any) => {
              if (obj.type === 'subtract' && obj.parent === clickedName) {
                if (obj.name && !relatedNames.includes(obj.name)) {
                  relatedNames.push(obj.name)
                }
              }
              // 也查找以 baseName_ 开头的对象
              if (obj.name && obj.name.startsWith(clickedName + '_') && !relatedNames.includes(obj.name)) {
                relatedNames.push(obj.name)
              }
            })
          }
        }
        
        // 过滤掉不存在的对象
        const validRelatedNames = relatedNames.filter(name => 
          name && name !== '' && objectDefinitions[name] && !deletedComponentNames.value.has(name)
        )
        
        // 确保至少包含原对象
        if (!validRelatedNames.includes(clickedName) && !deletedComponentNames.value.has(clickedName)) {
          validRelatedNames.unshift(clickedName)
        }
        
        // 处理选择逻辑（支持 Ctrl 多选）
        if (syntheticEvent.ctrlKey || syntheticEvent.metaKey) {
          // Ctrl + 双击：添加选择
          validRelatedNames.forEach(name => {
            if (!selectedComponentNames.value.includes(name)) {
              selectedComponentNames.value.push(name)
              setMeshHighlighted(name, true)
            }
          })
        } else {
          // 普通双击：替换选择
          // 清除所有已选中的高亮
          selectedComponentNames.value.forEach(selectedName => {
            setMeshHighlighted(selectedName, false)
          })
          
          // 选中所有相关对象
          selectedComponentNames.value = []
          validRelatedNames.forEach(name => {
            if (objectDefinitions[name] && !deletedComponentNames.value.has(name)) {
              selectedComponentNames.value.push(name)
              setMeshHighlighted(name, true)
            }
          })
        }
        
        updateScaleDisplay()
        updateCurrentColorDisplay()
        
        // 滚动到第一个组件
        if (selectedComponentNames.value.length > 0) {
          scrollToComponent(selectedComponentNames.value[0])
        }
        
        // 重置
        lastClickTime = 0
        lastClickObject = null
      } else {
        // 第一次点击，记录
        lastClickTime = currentTime
        lastClickObject = clickedObject
      }
    } else {
      // 点击了物体但没有名字，重置
      lastClickTime = 0
      lastClickObject = null
      hideScaleHandle() // 点击无名称物体时隐藏手柄
    }
  } else {
    // 点击空白区域，重置
    lastClickTime = 0
    lastClickObject = null
    hideScaleHandle()
  }
}

// 滚动到对应的组件
const scrollToComponent = (name: string) => {
  // 找到对应的组件元素并滚动到可见位置
  setTimeout(() => {
    const chipElements = document.querySelectorAll('.component-chip')
    chipElements.forEach((el) => {
      const chipName = el.querySelector('.chip-name')?.textContent
      if (chipName === name) {
        el.scrollIntoView({ behavior: 'smooth', block: 'center' })
      }
    })
  }, 100)
}

const getLocalMatrix = (obj: any) => {
  const matrix = new THREE.Matrix4()
  matrix.identity()

  if (obj.rotation) {
    const euler = new THREE.Euler(
      (obj.rotation[0] * Math.PI) / 180,
      (obj.rotation[1] * Math.PI) / 180,
      (obj.rotation[2] * Math.PI) / 180
    )
    const quat = new THREE.Quaternion()
    quat.setFromEuler(euler)
    const rotMatrix = new THREE.Matrix4()
    rotMatrix.makeRotationFromQuaternion(quat)
    matrix.multiply(rotMatrix)
  }

  if (obj.position) {
    matrix.setPosition(obj.position[0], obj.position[1], obj.position[2])
  }

  return matrix
}

const makeMaterial = (obj: any) => {
  const color = new THREE.Color(
    obj.color ? obj.color[0] : 0.8,
    obj.color ? obj.color[1] : 0.8,
    obj.color ? obj.color[2] : 0.8
  )
  const opacity = obj.opacity ?? 1
  const transparent = opacity < 1
  const isWindow = isGlassObjectName(obj.name)

  if (isWindow) {
    return new THREE.MeshPhysicalMaterial({
      color,
      transparent: true,
      opacity: opacity < 1 ? opacity : 0.35,
      transmission: 0.9,
      roughness: 0.08,
      metalness: 0,
      thickness: 0.02,
      attenuationColor: color,
      attenuationDistance: 0.7,
      side: THREE.DoubleSide,
      depthTest: true,
      depthWrite: false,
    })
  }

  const material = new THREE.MeshStandardMaterial({
    color,
    metalness: 0.1,
    roughness: 0.8,
    transparent,
    opacity,
    side: THREE.DoubleSide,
    depthTest: true,
    depthWrite: transparent ? false : true,
    alphaTest: transparent ? 0 : 0,
  })

  return material
}

const createRulerAxis = (
  length: number,
  direction: THREE.Vector3,
  color: number,
  majorTickSpacing: number,
  minorTickSpacing: number,
  majorTickSize: number,
  minorTickSize: number
) => {
  const points: THREE.Vector3[] = []
  const axisEnd = direction.clone().multiplyScalar(length)
  points.push(new THREE.Vector3(0, 0, 0), axisEnd)

  for (let pos = 0; pos <= length + 0.0001; pos += minorTickSpacing) {
    const tickCenter = direction.clone().multiplyScalar(pos)
    const tickOffset = new THREE.Vector3()
    const isMajor = Math.abs(pos % majorTickSpacing) < 0.0001
    const size = isMajor ? majorTickSize : minorTickSize

    if (Math.abs(direction.x) > 0) tickOffset.set(0, size, 0)
    else if (Math.abs(direction.y) > 0) tickOffset.set(size, 0, 0)
    else tickOffset.set(size, 0, 0)

    points.push(tickCenter.clone().sub(tickOffset))
    points.push(tickCenter.clone().add(tickOffset))
  }

  const geometry = new THREE.BufferGeometry().setFromPoints(points)
  const material = new THREE.LineBasicMaterial({
    color,
    transparent: true,
    opacity: 0.2,
    depthTest: true,
  })
  const line = new THREE.LineSegments(geometry, material)

  const group = new THREE.Group()
  group.add(line)
  return group
}

const updateCameraByKeyboard = () => {
  if (!camera || !controls) return

  const speed = 0.1
  const worldUp = new THREE.Vector3(0, 1, 0)
  const forward = new THREE.Vector3()
  camera.getWorldDirection(forward)
  forward.y = 0
  if (forward.lengthSq() < 1e-8) {
    forward.set(0, 0, -1)
  } else {
    forward.normalize()
  }
  const right = new THREE.Vector3().crossVectors(forward, worldUp).normalize()
  const move = new THREE.Vector3()

  if (keyState.KeyW || keyState.ArrowUp) {
    move.add(forward)
  }
  if (keyState.KeyS || keyState.ArrowDown) {
    move.sub(forward)
  }
  if (keyState.KeyA) {
    move.sub(right)
  }
  if (keyState.KeyD) {
    move.add(right)
  }

  if (move.lengthSq() > 0) {
    move.normalize().multiplyScalar(speed)
    camera.position.add(move)
    controls.target.add(move)
  }
}

const resize = () => {
  if (!container.value || !renderer || !camera) return
  const width = container.value.clientWidth
  const height = container.value.clientHeight
  camera.aspect = width / height
  camera.updateProjectionMatrix()
  renderer.setSize(width, height)
}

const animate = () => {
  if (!renderer || !scene || !camera || !controls) return
  updateCameraByKeyboard()
  controls.update()
  renderer.render(scene, camera)
  animationId = requestAnimationFrame(animate)
}

// 从场景中清理所有网格体（保留辅助对象如网格、坐标轴等）
const clearSceneMeshes = () => {
  if (!scene) return
  
  const objectsToRemove: THREE.Object3D[] = []
  scene.traverse((child) => {
    if (child instanceof Brush || 
        (child instanceof THREE.Mesh && !(child instanceof THREE.GridHelper) && 
         !(child instanceof THREE.AxesHelper))) {
      objectsToRemove.push(child)
    } else if (child instanceof THREE.Group && child.children.length > 0) {
      const hasLine = child.children.some(c => c instanceof THREE.LineSegments)
      if (!hasLine) {
        objectsToRemove.push(child)
      }
    }
  })
  
  objectsToRemove.forEach(obj => {
    scene?.remove(obj)
  })
  
  // 清理所有 box helpers
  Object.keys(selectionBoxHelpers).forEach(key => {
    const boxHelper = selectionBoxHelpers[key]
    if (boxHelper && scene) {
      scene.remove(boxHelper)
    }
    delete selectionBoxHelpers[key]
  })
}

// 使用指定数据构建场景
const buildSceneFromData = (data: { objects: any[] }, needClear: boolean) => {
  if (!scene) return
  
  // 清理场景
  clearSceneMeshes()
  
  // 清理数据结构
  Object.keys(objectDefinitions).forEach(key => delete objectDefinitions[key])
  Object.keys(meshByComponentName).forEach(key => delete meshByComponentName[key])
  Object.keys(originalSizes).forEach(key => delete originalSizes[key])
  movedObjects.clear()
  if(needClear) {
    selectedComponentNames.value = []
  }

  
  updateScaleDisplay()
  updateCurrentColorDisplay()
  
  // 初始化对象定义（过滤已删除的对象）
  data.objects.forEach((obj: any) => {
    if (obj.name && !deletedComponentNames.value.has(obj.name)) {
      objectDefinitions[obj.name] = JSON.parse(JSON.stringify(obj))
    }
  })
  
  // 初始化原始尺寸
  data.objects.forEach((obj: any) => {
    if (!obj.name || deletedComponentNames.value.has(obj.name)) return
    if (obj.type === 'cylinder') {
      originalSizes[obj.name] = [obj.radius, obj.height]
    } else if (obj.size) {
      originalSizes[obj.name] = [...obj.size] as [number, number, number]
    }
  })
  
  // 分类对象
  const evaluator = new Evaluator()
  const baseObjects: any[] = []
  const subtractOps: { [parent: string]: any[] } = {}
  const decorativeObjects: any[] = []
  
  data.objects.forEach((obj: any) => {
    if (!obj.name || deletedComponentNames.value.has(obj.name)) return
    
    if (obj.type === 'subtract') {
      // 检查父对象是否已被删除
      if (deletedComponentNames.value.has(obj.parent)) return
      
      if (!subtractOps[obj.parent]) {
        subtractOps[obj.parent] = []
      }
      subtractOps[obj.parent].push(obj)
    } else if (HIDE_WINDOW_MESHES && isGlassObjectName(obj.name)) {
      return
    } else if (isGlassObjectName(obj.name) || (obj.opacity !== undefined && obj.opacity < 1 && (obj.type === 'box' || obj.type === 'cylinder'))) {
      decorativeObjects.push(obj)
    } else if (obj.type === 'box' || obj.type === 'cylinder') {
      baseObjects.push(obj)
    }
  })
  
  const getMatrixForObject = (obj: any) => {
    return getWorldMatrix(obj)
  }
  
  // 构建基础对象（包含 CSG 减法）
  baseObjects.forEach((obj: any) => {
    let geom: THREE.BufferGeometry
    const material = makeMaterial(obj)

    if (obj.type === 'box') {
      geom = new THREE.BoxGeometry(obj.size[0], obj.size[1], obj.size[2])
    } else if (obj.type === 'cylinder') {
      geom = new THREE.CylinderGeometry(obj.radius, obj.radius, obj.height, 32)
    } else {
      return
    }

    const matrix = getMatrixForObject(obj)
    //geom.applyMatrix4(matrix)

    let result = new Brush(geom, material)
    matrix.decompose(result.position, result.quaternion, result.scale)
    result.updateMatrixWorld()

    if (subtractOps[obj.name]) {
      subtractOps[obj.name].forEach((sub: any) => {
        let subGeom: THREE.BufferGeometry
        if (sub.shape === 'box') {
          subGeom = new THREE.BoxGeometry(sub.size[0], sub.size[1], sub.size[2])
        } else if (sub.shape === 'cylinder') {
          subGeom = new THREE.CylinderGeometry(sub.radius, sub.radius, sub.height, 32)
        } else {
          return
        }

        const subMatrix = getMatrixForObject(sub)
        //subGeom.applyMatrix4(subMatrix)

        const subBrush = new Brush(
          subGeom,
          new THREE.MeshStandardMaterial({
            depthTest: true,
          })
        )
        subMatrix.decompose(subBrush.position, subBrush.quaternion, subBrush.scale)
        subBrush.updateMatrixWorld() 

        result = evaluator.evaluate(result, subBrush, SUBTRACTION)
      })
    }

    scene?.add(result)
    result.renderOrder = 0
    if (obj.name) {
      result.name = obj.name
      meshByComponentName[obj.name] = result
    }
  })
  
  // 构建装饰对象
  decorativeObjects.forEach((obj: any) => {
    let geom: THREE.BufferGeometry
    const material = makeMaterial(obj)

    if (obj.type === 'box') {
      geom = new THREE.BoxGeometry(obj.size[0], obj.size[1], obj.size[2])
    } else if (obj.type === 'cylinder') {
      geom = new THREE.CylinderGeometry(obj.radius, obj.radius, obj.height, 32)
    } else {
      return
    }

    const matrix = getMatrixForObject(obj)
    //geom.applyMatrix4(matrix)

    const mesh = new THREE.Mesh(geom, material)
    matrix.decompose(mesh.position, mesh.quaternion, mesh.scale)
    mesh.updateMatrixWorld() 

    
    mesh.renderOrder = obj.opacity !== undefined && obj.opacity < 1 ? 2 : 1
    if (obj.name) {
      mesh.name = obj.name
      meshByComponentName[obj.name] = mesh
    }
    scene?.add(mesh)
  })
 if(!needClear) {
    selectedComponentNames.value.forEach(name => {
    setMeshHighlighted(name, true)    
  })
 }
}

// 重建场景 - 使用 exportJSON 的数据
const rebuildScene = () => {
  hideScaleHandle() // 重建前隐藏手柄
  const exportData = getExportData()
  
  if (!exportData) {
    exportMessage.value = '❌ No data to rebuild from'
    if (exportTimeout) clearTimeout(exportTimeout)
    exportTimeout = setTimeout(() => { exportMessage.value = '' }, 3000)
    return
  }
  cachedJSON = exportData
  isLoading.value = true
  
  try {
    // 使用导出数据重建场景
    buildSceneFromData(cachedJSON, false)
    exportMessage.value = '✅ Scene rebuilt'
  } catch (error) {
    console.error('Failed to rebuild scene:', error)
    exportMessage.value = '❌ Failed to rebuild scene'
  } finally {
    isLoading.value = false
    if (exportTimeout) clearTimeout(exportTimeout)
    exportTimeout = setTimeout(() => { exportMessage.value = '' }, 3000)
  }
  console.log('Rebuild')
}

onMounted(async () => {
  if (!container.value) return

  const width = container.value.clientWidth
  const height = container.value.clientHeight

  scene = new THREE.Scene()
  scene.background = new THREE.Color(0x111827)

  camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000)
  camera.position.set(18, 12, 28)

  renderer = new THREE.WebGLRenderer({ antialias: true })
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
  renderer.setSize(width, height)
  renderer.sortObjects = true
  container.value.appendChild(renderer.domElement)

  const ambientLight = new THREE.AmbientLight(0xffffff, 0.6)
  scene.add(ambientLight)

  const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8)
  directionalLight.position.set(5, 10, 7.5)
  scene.add(directionalLight)

  // 添加辅助对象（这些不会被重建清除）
  const grid = new THREE.GridHelper(220, 22, 0x444444, 0x222222)
  scene.add(grid)

  const meterAxis = createRulerAxis(12, new THREE.Vector3(1, 0, 0), 0xff0000, 1, 0.1, 0.4, 0.15)
  meterAxis.position.set(0, 0.01, 0)
  scene.add(meterAxis)

  const yAxis = createRulerAxis(12, new THREE.Vector3(0, 1, 0), 0x00ff00, 1, 0.1, 0.4, 0.15)
  yAxis.position.set(0, 0.01, 0)
  scene.add(yAxis)

  const zAxis = createRulerAxis(12, new THREE.Vector3(0, 0, 1), 0x0000ff, 1, 0.1, 0.4, 0.15)
  zAxis.position.set(0, 0.01, 0)
  scene.add(zAxis)

  const axes = new THREE.AxesHelper(5)
  scene.add(axes)

  // 加载初始数据
  try {
    const response = await fetch('/house.json')
    const data = await response.json()

    cachedJSON = { objects: (data.objects ?? []).map((obj: any) => ({ ...obj })) }

    componentList.value = (data.objects ?? []).map((obj: any, index: number) => ({
      name: obj.name ?? `unnamed_${index}`,
      type: obj.type ?? 'unknown',
      parent: obj.parent,
    }))

    // 使用原始数据构建初始场景
    if (cachedJSON) {
      buildSceneFromData(cachedJSON, true)
    }
  } catch (error) {
    console.error('Failed to load bus.json:', error)
  }

  controls = new OrbitControls(camera!, renderer!.domElement)
  controls.enableDamping = true

  window.addEventListener('resize', resize)
  window.addEventListener('keydown', onKeyDown)
  window.addEventListener('keyup', onKeyUp)
  
  // 添加双击选择事件
  if (container.value) {
    container.value.addEventListener('mousedown', onMouseDown)
  }

  // ★ 新增全局 mousemove/mouseup 用于拖拽手柄
  window.addEventListener('mousemove', onMouseMove)
  window.addEventListener('mouseup', onMouseUp)
  
  animate()
})

onBeforeUnmount(() => {
  if (animationId) cancelAnimationFrame(animationId)
  window.removeEventListener('resize', resize)
  window.removeEventListener('keydown', onKeyDown)
  window.removeEventListener('keyup', onKeyUp)
  
  // 移除双击选择事件
  if (container.value) {
    container.value.removeEventListener('mousedown', onMouseDown)
  }

  // ★ 移除全局拖拽事件
  window.removeEventListener('mousemove', onMouseMove)
  window.removeEventListener('mouseup', onMouseUp)

  // 清理所有包围盒
  Object.keys(selectionBoxHelpers).forEach(key => {
    const boxHelper = selectionBoxHelpers[key]
    if (boxHelper && scene) {
      scene.remove(boxHelper)
    }
    delete selectionBoxHelpers[key]
  })

  // 清理伸缩手柄
  hideScaleHandle()

  if (renderer && renderer.domElement.parentNode) {
    renderer.domElement.parentNode.removeChild(renderer.domElement)
  }

  renderer = null
  scene = null
  camera = null
  controls = null
})
</script>

<style scoped>
.scene-root {
  width: 100%;
  min-height: 100vh;
  position: relative;
  overflow: hidden;
}

.panels-wrapper {
  position: fixed;
  left: 0;
  top: 0;
  bottom: 0;
  display: flex;
  z-index: 20;
}

.component-panel {
  width: 280px;
  background: #0f172a;
  color: #e2e8f0;
  padding: 12px;
  box-sizing: border-box;
  overflow-y: auto;
  height: 100%;
}

/* 左侧第一列：组件列表 */
.left-panel {
  border-right: 1px solid #1e293b;
}

/* 左侧第二列：变换控制 */
.transform-panel {
  width: 240px;
  border-right: 1px solid #1e293b;
}

.panel-title {
  font-size: 16px;
  font-weight: 700;
  margin-bottom: 8px;
}

.panel-count {
  margin-top: 4px;
  margin-bottom: 10px;
  color: #94a3b8;
  font-size: 12px;
}

.selected-count {
  color: #22c55e;
  font-weight: 600;
}

.filter-box {
  position: relative;
  margin-bottom: 10px;
}

.filter-input {
  width: 100%;
  padding: 8px 32px 8px 10px;
  border-radius: 6px;
  border: 1px solid #1f2937;
  background: #111827;
  color: #e2e8f0;
  font-size: 13px;
  outline: none;
  box-sizing: border-box;
  transition: border-color 0.15s ease;
}

.filter-input:focus {
  border-color: #22c55e;
}

.filter-input::placeholder {
  color: #64748b;
}

.filter-clear {
  position: absolute;
  right: 6px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: #94a3b8;
  cursor: pointer;
  font-size: 14px;
  padding: 2px 6px;
  border-radius: 3px;
  transition: color 0.15s ease, background-color 0.15s ease;
}

.filter-clear:hover {
  color: #e2e8f0;
  background: #1e293b;
}

.rebuild-section {
  margin-bottom: 10px;
}

.rebuild-btn {
  width: 100%;
  padding: 10px 0;
  border-radius: 6px;
  border: 1px solid #3b82f6;
  background: #0a1a3a;
  color: #3b82f6;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: background-color 0.3s ease, border-color 0.3s ease, opacity 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.rebuild-btn:hover {
  background: #0d1f4a;
  border-color: #60a5fa;
  color: #60a5fa;
}

.rebuild-btn:active {
  background: #071430;
  transform: scale(0.98);
}

.rebuild-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  background: #1a1a2e;
  border-color: #334155;
  color: #64748b;
  transform: none;
}

.action-buttons {
  margin-bottom: 10px;
}

.delete-selection-btn {
  width: 100%;
  padding: 8px 0;
  border-radius: 6px;
  border: 1px solid #f59e0b;
  background: #1a140a;
  color: #f59e0b;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 8px;
  transition: background-color 0.15s ease;
}

.delete-selection-btn:hover {
  background: #2d1f0a;
}

.clear-selection-btn {
  width: 100%;
  padding: 8px 0;
  border-radius: 6px;
  border: 1px solid #ef4444;
  background: #1a0f0f;
  color: #ef4444;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 8px;
  transition: background-color 0.15s ease;
}

.clear-selection-btn:hover {
  background: #2d1515;
}

.export-btn {
  width: 100%;
  padding: 8px 0;
  border-radius: 6px;
  border: 1px solid #22c55e;
  background: #052e16;
  color: #22c55e;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: background-color 0.15s ease;
}

.export-btn:hover {
  background: #064e1b;
}

.export-msg {
  margin-top: 6px;
  font-size: 12px;
  color: #22c55e;
  text-align: center;
}

.component-flow {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.component-chip {
  background: #111827;
  border: 1px solid #1f2937;
  border-radius: 6px;
  padding: 8px;
  display: flex;
  flex-direction: column;
  gap: 2px;
  max-width: 100%;
  cursor: pointer;
  transition: border-color 0.15s ease, background-color 0.15s ease;
}

.component-chip.selected {
  border-color: #22c55e;
  background: #052e16;
}

.component-chip.deleted {
  opacity: 0.3;
  text-decoration: line-through;
}

.chip-name {
  font-size: 13px;
  font-weight: 600;
  word-break: break-word;
}

.chip-type,
.chip-parent {
  font-size: 11px;
  color: #94a3b8;
  word-break: break-word;
}

/* 变换面板样式 */
.transform-section {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.transform-group {
  margin-bottom: 4px;
}

.transform-group-title {
  font-size: 14px;
  font-weight: 700;
  color: #22c55e;
  margin-bottom: 8px;
  padding-bottom: 4px;
  border-bottom: 1px solid #1e293b;
}

.transform-title-info {
  font-size: 12px;
  color: #94a3b8;
  margin-bottom: 10px;
  word-break: break-word;
}

.transform-scale-display {
  font-size: 16px;
  font-weight: 600;
  color: #e2e8f0;
  margin-bottom: 10px;
  padding: 4px 8px;
  background: #1a1a2e;
  border-radius: 4px;
  text-align: center;
}

.transform-row {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 6px;
}

.axis-label {
  width: 20px;
  text-align: center;
  font-size: 13px;
  font-weight: 700;
  color: #64748b;
}

.axis-x {
  color: #ef4444;
}

.axis-y {
  color: #22c55e;
}

.axis-z {
  color: #3b82f6;
}

.dir-btn {
  flex: 1;
  padding: 6px 0;
  border-radius: 4px;
  border: 1px solid #1f2937;
  background: #0f172a;
  color: #e2e8f0;
  cursor: pointer;
  font-size: 13px;
  font-weight: 600;
  transition: background-color 0.15s ease, border-color 0.15s ease;
}

.dir-btn:hover {
  background: #1e293b;
  border-color: #22c55e;
}

.transform-step {
  margin-top: 8px;
  font-size: 12px;
  color: #94a3b8;
}

.step-select {
  margin-left: 4px;
  padding: 2px 4px;
  border-radius: 4px;
  border: 1px solid #1f2937;
  background: #0f172a;
  color: #e2e8f0;
  font-size: 12px;
  outline: none;
}

.transform-divider {
  height: 1px;
  background: #1e293b;
  margin: 12px 0;
}

/* ============ 颜色面板样式 ============ */

.color-picker-section {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.color-preview-row {
  display: flex;
  align-items: center;
  gap: 10px;
}

.color-input-label {
  cursor: pointer;
  position: relative;
  display: inline-block;
}

.color-preview {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  border: 2px solid #334155;
  cursor: pointer;
  transition: border-color 0.2s;
}

.color-preview:hover {
  border-color: #22c55e;
}

.color-picker-input {
  position: absolute;
  top: 0;
  left: 0;
  width: 48px;
  height: 48px;
  padding: 0;
  border: none;
  opacity: 0;
  cursor: pointer;
}

.color-hex {
  font-size: 14px;
  font-weight: 600;
  color: #94a3b8;
  font-family: monospace;
  letter-spacing: 1px;
}

.color-rgb-values {
  display: flex;
  gap: 10px;
  font-size: 11px;
  color: #64748b;
  font-family: monospace;
}

.preset-colors {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  padding: 4px 0;
}

.preset-color-dot {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  border: 2px solid #334155;
  cursor: pointer;
  transition: transform 0.15s, border-color 0.15s;
}

.preset-color-dot:hover {
  transform: scale(1.2);
  border-color: #22c55e;
}

.reset-color-btn {
  width: 100%;
  padding: 6px 0;
  border-radius: 6px;
  border: 1px solid #64748b;
  background: #0f172a;
  color: #94a3b8;
  cursor: pointer;
  font-size: 12px;
  transition: background-color 0.15s, color 0.15s;
}

.reset-color-btn:hover {
  background: #1e293b;
  color: #e2e8f0;
  border-color: #ef4444;
}

.no-selection-hint {
  font-size: 12px;
  color: #475569;
  text-align: center;
  padding: 16px 0;
  font-style: italic;
}


/* 响应式布局 */
@media (max-width: 1100px) {
  .transform-panel {
    display: none;
  }
  
  .left-panel {
    width: 260px;
  }
}
.canvas-container {
  position: fixed;      /* 或者 absolute，反正面板也是 fixed */
  left: 520px;          /* 左侧两个面板的总宽度 (280px + 240px) */
  top: 0;
  right: 0;
  bottom: 0;
  overflow: hidden;
}
canvas {
  display: block;
  width: 100% !important;
  height: 100% !important;
}
</style>