from mmm.pianorolls.music import TimeShift, FrequencyPoint
from mmm.pianorolls.generation import Hit, Rhythm, Texture, Chord

t_1 = Texture([
    Rhythm([Hit(TimeShift(0, 16), TimeShift(1, 16))]),
    Rhythm([Hit(TimeShift(1, 16), TimeShift(5, 16))]),
    Rhythm([Hit(TimeShift(2, 16), TimeShift(1, 16))]),
    Rhythm([Hit(TimeShift(3, 16), TimeShift(1, 16))])
])

d_min = Chord([FrequencyPoint(50), FrequencyPoint(57), FrequencyPoint(62), FrequencyPoint(65)])

d_min_1 = t_1 * d_min
