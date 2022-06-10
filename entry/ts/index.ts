import * as THREE from 'three'
//import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader'
import { VRM, VRMSchema, VRMUnlitMaterial } from '@pixiv/three-vrm'
import { convertToObject } from 'typescript';
import { mode } from '../../webpack.config';
import { randInt } from 'three/src/math/MathUtils';

window.addEventListener("DOMContentLoaded", () => {
    // canvasの取得
    var canvas = <HTMLCanvasElement>document.getElementById('canvas');

    // modelpathのリスト
    var modelPass = '../static/base_model/Salieri.vrm';
    const modelSarieli = '../static/base_model/Salieri.vrm';
    const modelKurisu = '../static/base_model/kurisu.vrm';
    const modelbase = '../static/base_model/base.vrm';

    //posepathのリスト
    var posepass = '../static/pose/hellovrm.csv';
    const pose_hello = '../static/pose/hellovrm.csv';
    const pose_ozigi = '../static/pose/ozigi.csv';
    const pose_suneru = '../static/pose/suneru.csv';
    const pose_doya = '../static/pose/doya.csv';
    const pose_leftHand = '../static/pose/leftHand.csv';

    // シーンの設定
    const scene = new THREE.Scene()
    sceneOption()

    function sceneOption() {
        // ライトの設定
        const light = new THREE.DirectionalLight(0xffffff)
        light.position.set(1, 1, 1).normalize()
        scene.add(light)
    }

    // レンダラーの設定
    const renderer = new THREE.WebGLRenderer({
        canvas: <HTMLCanvasElement>document.querySelector('#canvas'),
        antialias: true,
        alpha: true,
        preserveDrawingBuffer: true,
    })
    renderer.setSize(canvas.clientWidth, canvas.clientHeight)
    renderer.setPixelRatio(window.devicePixelRatio)

    // カメラの設定
    const camera = new THREE.PerspectiveCamera(
        35,
        canvas.clientWidth / canvas.clientHeight,
        0.1,
        1000,
    )
    camera.position.set(0, 1, 1.8)
    camera.lookAt(0, 1.1, 0)

    // VRMの読み込み
    var boneNode: any = []
    var faceNode: any = []
    let mixer: any
    const loader = new GLTFLoader()
    newLoad()

    function newLoad() {
        loader.load(modelPass,
            (gltf) => {
                VRM.from(gltf).then((vrm: any) => {
                    // シーンへの追加
                    scene.add(vrm.scene)
                    vrm.scene.rotation.y = Math.PI
                    setupAnimation(vrm)
                    makeAnimation(pose_hello);
                })
            }
        )
    }

    // http → str
    const http2str = (url: string) => {
        try {
            let request = new XMLHttpRequest()
            request.open("GET", url, false)
            request.send(null)
            if (request.status == 200 && request.readyState == 4) {
                return request.responseText.trim()
            }
        } catch (e) {
            console.log(e)
        }
        return ""
    }

    // CSV → hierarchy
    const csv2hierarchy = (csv: string, fps: number) => {
        // 文字列 → 配列
        let lines = csv.trim().split('\n')
        let data: number[][] = []
        for (let j = 0; j < lines.length; j++) {
            data[j] = []
            let strs = lines[j].split(',')
            for (let i = 0; i < 55 * 4; i++) {
                data[j][i] = Number(strs[i])
            }
        }
        // 配列 → hierarchy
        let hierarchy = []
        for (let i = 0; i < 55; i++) {
            let keys = []
            for (let j = 0; j < data.length; j++) {
                keys[j] = {
                    rot: new THREE.Quaternion(-data[j][i * 4], -data[j][i * 4 + 1], data[j][i * 4 + 2], data[j][i * 4 + 3]).toArray(),
                    time: fps * j
                }
            }
            hierarchy[i] = { 'keys': keys }
        }
        //小町ちゃん用のsplice
        hierarchy.splice(54, 1)
        hierarchy.splice(23, 1)
        hierarchy.splice(22, 1)
        hierarchy.splice(21, 1)
        return hierarchy
    }

    // アニメーションの初期設定
    const setupAnimation = (vrm: any) => {
        mixer = new THREE.AnimationMixer(vrm.scene)
        // ボーンリストの生成 boneの数を変更した場合、csv2hierarchyの中身を変更すること
        //顎目胸抜き
        const bones = ["hips", "leftUpperLeg", "rightUpperLeg", "leftLowerLeg", "rightLowerLeg", "leftFoot", "rightFoot", "spine", "chest", "neck", "head", "leftShoulder", "rightShoulder", "leftUpperArm", "rightUpperArm", "leftLowerArm", "rightLowerArm", "leftHand", "rightHand", "leftToes", "rightToes", "leftThumbProximal", "leftThumbIntermediate", "leftThumbDistal", "leftIndexProximal", "leftIndexIntermediate", "leftIndexDistal", "leftMiddleProximal", "leftMiddleIntermediate", "leftMiddleDistal", "leftRingProximal", "leftRingIntermediate", "leftRingDistal", "leftLittleProximal", "leftLittleIntermediate", "leftLittleDistal", "rightThumbProximal", "rightThumbIntermediate", "rightThumbDistal", "rightIndexProximal", "rightIndexIntermediate", "rightIndexDistal", "rightMiddleProximal", "rightMiddleIntermediate", "rightMiddleDistal", "rightRingProximal", "rightRingIntermediate", "rightRingDistal", "rightLittleProximal", "rightLittleIntermediate", "rightLittleDistal"]

        //最低限bone
        //const bones = ["hips", "leftUpperLeg", "rightUpperLeg", "leftLowerLeg", "rightLowerLeg", "leftFoot", "rightFoot", "spine", "chest", "neck", "head", "leftUpperArm", "rightUpperArm", "leftLowerArm", "rightLowerArm", "leftHand", "rightHand"]
        for (let i = 0; i < bones.length; i++) {
            boneNode[i] = vrm.humanoid.getBoneNode(bones[i])
        }
        faceNode = vrm.blendShapeProxy //表情読み込む用のやつ
        //vrm.blendShapeProxy.setValue(VRMSchema.BlendShapePresetName.Joy, 1.0)
        vrm.blendShapeProxy.update()
    }

    //アニメーションをセットする
    const makeAnimation = (posepass: string) => {
        // AnimationClipの生成
        const clip = THREE.AnimationClip.parseAnimation({
            hierarchy: csv2hierarchy(http2str(posepass), 200)
        }, boneNode)
        // トラック名の変更
        clip.tracks.some((track) => {
            track.name = track.name.replace(/^\.bones\[([^\]]+)\].(position|quaternion|scale)$/, '$1.$2')
        })
        //前のアニメをストップ
        mixer.stopAllAction();
        //AnimationActionの生成とアニメーションの再生
        let action = mixer.clipAction(clip)
        action.play()
    }

    const resetFaceNode = (faceNode: any) => {
        faceNode.setValue(VRMSchema.BlendShapePresetName.Angry, 0)
        faceNode.setValue(VRMSchema.BlendShapePresetName.Fun, 0)
        faceNode.setValue(VRMSchema.BlendShapePresetName.Joy, 0)
        faceNode.setValue(VRMSchema.BlendShapePresetName.Sorrow, 0)
        faceNode.setValue(VRMSchema.BlendShapePresetName.A, 0)
        faceNode.setValue(VRMSchema.BlendShapePresetName.I, 0)
        faceNode.setValue(VRMSchema.BlendShapePresetName.U, 0)
        faceNode.setValue(VRMSchema.BlendShapePresetName.E, 0)
        faceNode.setValue(VRMSchema.BlendShapePresetName.O, 0)
    }

    //変数宣言
    let lastTime = (new Date()).getTime()
    let currentPose = "";
    let currentModel = "salieri";
    let currentMouth = "false";
    let newPose = <HTMLInputElement>document.getElementById('vuePose');
    let newModel = <HTMLInputElement>document.getElementById('vueModel');
    let newMouth = <HTMLInputElement>document.getElementById('vueMouth');
    let poseChangeCount = 0;
    let mouthCnt = 0;

    // フレーム毎に呼ばれる関数
    const update = () => {
        requestAnimationFrame(update)

        // 時間計測
        let time = (new Date()).getTime()
        let delta = time - lastTime;
        poseChangeCount += 1;

        //html側から変数が代入されていると分岐
        if (currentPose != String(newPose.value) || currentModel != String(newModel.value)) {
            if (mixer != null) { resetFaceNode(faceNode) }

            //モデルの変更
            if (String(newModel.value) == "kurisu" && currentModel !== "kurisu") {
                scene.remove.apply(scene, scene.children);
                modelPass = modelKurisu;
                newLoad()
                sceneOption()
                camera.lookAt(0, 1.2, 0)
            }
            if (String(newModel.value) == "udon" && currentModel !== "udon") {
                scene.remove.apply(scene, scene.children);
                modelPass = modelbase;
                newLoad()
                sceneOption()
                camera.lookAt(0, 1.2, 0)
            }
            if (String(newModel.value) == "salieri" && currentModel !== "salieri") {
                scene.remove.apply(scene, scene.children);
                modelPass = modelSarieli;
                newLoad()
                sceneOption()
                camera.lookAt(0, 1.1, 0)
            }

            //ポーズの変更
            if (String(newPose.value) == "doya") {
                posepass = pose_doya
                faceNode.setValue(VRMSchema.BlendShapePresetName.Joy, 0.08)
                faceNode.setValue(VRMSchema.BlendShapePresetName.Fun, 0.64)
                faceNode.update()
                makeAnimation(posepass)
            } else if (String(newPose.value) == "leftHand") {
                posepass = pose_leftHand
                makeAnimation(posepass)
            }
            currentPose = String(newPose.value)
            currentModel = String(newModel.value)
            poseChangeCount = -1200
        }

        //20秒ごとにポーズを変えるためのswitch文
        if (poseChangeCount > 1200) {
            switch (getRandam(1, 4)) {
                case 1:
                    makeAnimation(pose_doya)
                    break;
                case 2:
                    makeAnimation(pose_hello)
                    break;
                case 3:
                    makeAnimation(pose_leftHand)
                    break;
                case 4:
                    makeAnimation(pose_ozigi)
                    break;
            }
            poseChangeCount = 0;
        }

        if (String(newMouth.value) == 'true') {
            mouthCnt += 1;
            let mouthHeight = mouthCnt * 4;
            if (mouthHeight > 60) {
                mouthHeight = (120 - mouthHeight);
            }
            mouthHeight = mouthHeight / 100;

            if (mixer != null) {
                faceNode.setValue(VRMSchema.BlendShapePresetName.A, mouthHeight);
                faceNode.update();
            }
            if (mouthCnt > 30) {
                mouthCnt = 0;
                currentMouth = String(newMouth.value)
            }

        } else if (currentMouth != String(newMouth.value)) {
            faceNode.setValue(VRMSchema.BlendShapePresetName.A, 0);
            faceNode.update();
            currentMouth = String(newMouth.value)
        }

        // アニメーションの定期処理
        if (mixer) {
            mixer.update(delta)
        }
        // 最終更新時間
        lastTime = time;

        // レンダリング
        renderer.render(scene, camera)
    }
    update()
})

function getRandam(n: number, m: number) {
    for (let i = 0; i < 5; i++) {
        let num = Math.floor(Math.random() * (m + 1 - n)) + n;
        return num;
    }
};