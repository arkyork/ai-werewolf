using UnityEngine;
using System.Collections; // Coroutineを使うために必要

public class AnimationLooper : MonoBehaviour
{
    public float delayBeforeRepeat = 3.0f; // アニメーションを繰り返すまでの遅延時間（秒）
    private Animator animator; // このGameObjectのアニメーターコンポーネント

    void Start()
    {
        // このGameObjectにアタッチされているAnimatorコンポーネントを取得
        animator = GetComponent<Animator>();

        // アニメーションの再生を開始
        PlaySittingAnimation();
    }

    void Update()
    {
        // Animatorが現在再生しているステートの情報を取得
        AnimatorStateInfo stateInfo = animator.GetCurrentAnimatorStateInfo(0);

        // "Sitting"という名前のアニメーション（ステート）が再生中で、かつ
        // そのアニメーションがほぼ終了に近づいている（正規化された時間が0.99以上）場合
        // ※アニメーションクリップのLoop Timeがオフになっている前提
        if (stateInfo.IsName("Sitting_crap_data") && stateInfo.normalizedTime >= 0.99f && !animator.IsInTransition(0))
        {
            // ここでコルーチンを開始して遅延させる
            StartCoroutine(RestartAnimationWithDelay());
        }
    }

    // 指定した遅延時間の後にアニメーションを再生し直すコルーチン
    IEnumerator RestartAnimationWithDelay()
    {
        // 現在実行中のコルーチンを停止して、重複実行を防ぐ（重要）
        StopAllCoroutines();

        // 指定された時間だけ待機
        yield return new WaitForSeconds(delayBeforeRepeat);

        // アニメーションを再生し直す
        PlaySittingAnimation();
    }

    // アニメーションを再生するメソッド
    void PlaySittingAnimation()
    {
        // Animatorのトリガーを設定して、アニメーションを再生
        // "PlayAnimation"はAnimatorで設定したトリガーの名前
        animator.SetTrigger("PlayAnimation");
    }
}