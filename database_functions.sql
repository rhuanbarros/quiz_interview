
-- acabei nao usando
CREATE OR REPLACE FUNCTION public.get_question_by_session(p_session_id TEXT)
RETURNS TABLE (
  id bigint,
  created_at timestamp with time zone,
  subject_matter TEXT,
  topic_description TEXT,
  level TEXT,
  question TEXT,
  type TEXT,
  answer_correct TEXT,
  explanation TEXT,
  answer_a TEXT,
  answer_b TEXT,
  answer_c TEXT,
  answer_d TEXT,
  session_id TEXT
) 
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN QUERY
  SELECT 
    question.id,
    question.created_at,
    question.subject_matter,
    question.topic_description,
    question.level,
    question.question,
    question.type,
    question.answer_correct,
    question.explanation,
    question.answer_a,
    question.answer_b,
    question.answer_c,
    question.answer_d,
    answer.session_id
  FROM
    question
    LEFT JOIN answer ON question.id = answer.question_id
  WHERE
    answer.session_id IS NULL OR 
    answer.session_id != p_session_id
  ORDER BY 
    RANDOM()
  LIMIT 1;
END;
$$;

