using UnityEngine;
using System.Collections; // Coroutine���g�����߂ɕK�v

public class AnimationLooper : MonoBehaviour
{
    public float delayBeforeRepeat = 3.0f; // �A�j���[�V�������J��Ԃ��܂ł̒x�����ԁi�b�j
    private Animator animator; // ����GameObject�̃A�j���[�^�[�R���|�[�l���g

    void Start()
    {
        // ����GameObject�ɃA�^�b�`����Ă���Animator�R���|�[�l���g���擾
        animator = GetComponent<Animator>();

        // �A�j���[�V�����̍Đ����J�n
        PlaySittingAnimation();
    }

    void Update()
    {
        // Animator�����ݍĐ����Ă���X�e�[�g�̏����擾
        AnimatorStateInfo stateInfo = animator.GetCurrentAnimatorStateInfo(0);

        // "Sitting"�Ƃ������O�̃A�j���[�V�����i�X�e�[�g�j���Đ����ŁA����
        // ���̃A�j���[�V�������قڏI���ɋ߂Â��Ă���i���K�����ꂽ���Ԃ�0.99�ȏ�j�ꍇ
        // ���A�j���[�V�����N���b�v��Loop Time���I�t�ɂȂ��Ă���O��
        if (stateInfo.IsName("Sitting_crap_data") && stateInfo.normalizedTime >= 0.99f && !animator.IsInTransition(0))
        {
            // �����ŃR���[�`�����J�n���Ēx��������
            StartCoroutine(RestartAnimationWithDelay());
        }
    }

    // �w�肵���x�����Ԃ̌�ɃA�j���[�V�������Đ��������R���[�`��
    IEnumerator RestartAnimationWithDelay()
    {
        // ���ݎ��s���̃R���[�`�����~���āA�d�����s��h���i�d�v�j
        StopAllCoroutines();

        // �w�肳�ꂽ���Ԃ����ҋ@
        yield return new WaitForSeconds(delayBeforeRepeat);

        // �A�j���[�V�������Đ�������
        PlaySittingAnimation();
    }

    // �A�j���[�V�������Đ����郁�\�b�h
    void PlaySittingAnimation()
    {
        // Animator�̃g���K�[��ݒ肵�āA�A�j���[�V�������Đ�
        // "PlayAnimation"��Animator�Őݒ肵���g���K�[�̖��O
        animator.SetTrigger("PlayAnimation");
    }
}